from ...Proposals.Proposal import ProposalBuilder
from ...Proposals.APIKeys import PROPOSAL_ID as PROPOSAL_ID_API
from ...Proposals.APIKeys import PI_LASTNAME
from .Consts import *
from ..Beamline.Ingestion import AbstractIngestor
from ..Beamline.ConfigKeys import *
from ..Beamline.Consts import RAW
from ...Datasets.DatasetVirtual import SCAMAGDatasetBuilder
from ...Datasets.APIKeys import SOURCE_FOLDER
from ...Filesystem.FSInfo import list_dirs, list_files, get_creation_date, folder_total_size
from ...Filesystem.FSInfoUnix import get_ownername
from ...Filesystem.ImInfo import load_numpy_from_image
from ...Datasets.Dataset import AttachmentBuilder, ScientificMetadataBuilder
from ...Samples.Sample import SampleBuilder, SampleCharacteristicsBuilder
from ...REST.Consts import NA
from ...REST import API
import pydicom


class SCAMAGIngestor(AbstractIngestor):
    def __init__(self, args):
        config = {
            CONFIG_LOG_SUFFIX: LOG_SUFFIX,
            CONFIG_LOG_FILENAMES: LOG_FILENAMES,
            CONFIG_LOCATION: LOCATION,
            CONFIG_KEYWORDS: KEYWORDS,
            CONFIG_SOURCE_PATH: SOURCE_PATH,
            CONFIG_PREFIX: SITE_PREFIX,
            CONFIG_FILENAME_IGNORE: FILENAME_IGNORE_PATTERN,
            CONFIG_DATASET_NAME: DATASET_NAME_PATTERN
        }
        super().__init__(args, config, SCAMAGDatasetBuilder, None, None)


    def _add_dcm_info_to_dict(self, dic, dcm_dir, study, series, dcm_meta, filename, day, date):
        if dcm_dir in dic.keys():
            dic = dic[dcm_dir]
            if study in dic.keys():
                dic = dic[study]
                if series in dic.keys():
                    dic = dic[series]
                    dic['day'] = day
                    dic['date'] = date
                    dic['meta'] = dcm_meta
                    if 'path' in dic.keys():
                        assert dic['path'] == dcm_dir, "{} != {}".format(dic['path'], dcm_dir)
                    dic['path'] = dcm_dir
                    if 'files' in dic.keys():
                        dic['files'].append(filename)
                    else:
                        dic['files'] = [filename]
                else:
                    dic[series] = {'meta': dcm_meta, 'path': dcm_dir, 'files': [filename], 'day': day, 'date': date}
            else:
                dic[study] = {series: {'meta': dcm_meta, 'path': dcm_dir, 'files': [filename], 'day': day, 'date': date}}
        else:
            dic[dcm_dir] = {study: {series: {'meta': dcm_meta, 'path': dcm_dir, 'files': [filename], 'day': day, 'date': date}}}


    def ingest_experiment(self):
        failed = {}

        proposal_dict = ProposalBuilder().\
            args(self.args).\
            proposal_id(PROPOSAL_ID).\
            pi_email(NA).\
            pi_lastname(NA).\
            email(NA).\
            abstract(PROPOSAL_ABSTRACT).\
            title(PROPOSAL_TITLE).\
            start_time(PROPOSAL_START).\
            end_time(PROPOSAL_END).\
            build()
        resp = API.proposal_ingest(self.args.token, proposal_dict, self.args.simulation, self.args.verbose)
        if resp.status_code != 200:
            failed[proposal_dict[PROPOSAL_ID_API]] = resp.text
        
        for pat_dir in sorted(list_dirs(self.config[CONFIG_SOURCE_PATH])):
            scb = SampleCharacteristicsBuilder()
            scb.add('Patient', pat_dir)
            scb.add('Location', 'MHH')
            sb = SampleBuilder(pat_dir).\
                     owner_group("hasylab").\
                     characteristics(scb.build()).\
                     description("SCAMAG Patient 1")
            data = sb.build()

            resp = API.ingest(self.args.token, "Samples", data, self.args.simulation, self.args.verbose)
            if resp.status_code != 200:
                failed[pat_dir] = resp.text

            patient_directory = "{}/{}".format(self.config[CONFIG_SOURCE_PATH], pat_dir)
            datasets = {}
            for long_dir in sorted(list_dirs(patient_directory)):
                longitudinal_directory = "{}/{}".format(patient_directory, long_dir)
                
                day = PAT1_DAY_MAPPING[long_dir]
                date = PAT1_DATE_MAPPING[long_dir]

                dcm_files = list_files(longitudinal_directory, exts=self.args.extensions)
                n_files = len(dcm_files)

                for f in dcm_files:
                    dcm_full_path = longitudinal_directory + "/" + f
                    dcm_meta = pydicom.dcmread(dcm_full_path)
                    self._add_dcm_info_to_dict(datasets, longitudinal_directory, dcm_meta.StudyID, dcm_meta.SeriesNumber, dcm_meta, f, day, date)

            for long_dir, long_dir_dict in datasets.items():
                for study, study_dict in long_dir_dict.items():
                    for series, series_dict in study_dict.items():

                        # Add raw dataset
                        smb = ScientificMetadataBuilder()
                        smb.set_value("Day after implant", series_dict['day'])
                        smb.set_value("Date of Image", series_dict['date'])

                        images_in_folder = sorted(series_dict['files'])
                        directory = series_dict['path']
                        total_size = folder_total_size(directory)
                        meta_info_file = "{}/{}".format(directory, images_in_folder[0])
                        creation_time = get_creation_date(meta_info_file)
                        dicom_meta = pydicom.dcmread(meta_info_file)

                        for tag in DICOM_TAGS:
                            value = dicom_meta.get(tag, NA)
                            if isinstance(value, list):
                                value = ",".join([str(v) for v in value])
                            smb.set_value("DICOM_" + tag, value)

                        sample_id = pat_dir

                        dataset_name = self.config[CONFIG_DATASET_NAME].format(self.config[CONFIG_PREFIX], sample_id, series_dict['day'], dicom_meta.get('Modality','?'), series, RAW)

                        dsb = self.raw_dataset_builder(base_keywords=self.config[CONFIG_KEYWORDS]).\
                            args(self.args).\
                            proposal_id(proposal_dict[PROPOSAL_ID_API]).\
                            owner(get_ownername(directory)).\
                            source_folder(directory).\
                            is_published(self.args.publish).\
                            size(total_size).\
                            principal_investigator(proposal_dict[PI_LASTNAME]).\
                            dataset_name(dataset_name).\
                            creation_location(self.config[CONFIG_LOCATION]).\
                            creation_time(creation_time).\
                            scientific_metadata(smb.build()).\
                            number_of_files(len(images_in_folder))

                        if sample_id is not None:
                            dsb.sample_id(sample_id)

                        dataset_dict = dsb.build()
                        filename_list = images_in_folder

                        datablock_dict = self._create_origdatablock(filename_list, dataset_dict)
                        attachment_dicts, failed_attachments = self._create_attachments(filename_list, dataset_dict, proposal_dict[PROPOSAL_ID_API])
                        failed.update(failed_attachments)
                        failed.update(self._api_dataset_ingest(dataset_dict, datablock_dict, attachment_dicts))


        if failed:    
            print("\n---!--- FAILURES ---!---")
            for key in sorted(failed.keys()):
                print("\n=>", key, "\n", failed[key], "\n")
        
