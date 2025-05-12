# Copyright (c) Alibaba, Inc. and its affiliates.
from modelscope.msdatasets.dataset_cls.custom_datasets import CUSTOM_DATASETS
from modelscope.msdatasets.dataset_cls.custom_datasets.easycv_base import \
    EasyCVBaseDataset
from modelscope.utils.constant import Tasks

from easycv.datasets.pose import \
    WholeBodyCocoTopDownDataset as _WholeBodyCocoTopDownDataset
from easycv.toolkit.modelscope.metainfo import \
    EasyCVCustomDatasets as CustomDatasets


@CUSTOM_DATASETS.register_module(
    group_key=Tasks.human_wholebody_keypoint,
    module_name=CustomDatasets.HumanWholeBodyKeypointDataset)
class WholeBodyCocoTopDownDataset(EasyCVBaseDataset,
                                  _WholeBodyCocoTopDownDataset):
    """EasyCV dataset for human whole body 2d keypoints.

    Args:
        split_config (dict): Dataset root path from MSDataset, e.g.
            {"train":"local cache path"} or {"evaluation":"local cache path"}.
        preprocessor (Preprocessor): An optional preprocessor instance, please make sure the preprocessor fits for
            the model if supplied. Not support yet.
        mode: Training or Evaluation.
    """

    def __init__(self,
                 split_config=None,
                 preprocessor=None,
                 mode=None,
                 *args,
                 **kwargs) -> None:
        EasyCVBaseDataset.__init__(
            self,
            split_config=split_config,
            preprocessor=preprocessor,
            mode=mode,
            args=args,
            kwargs=kwargs)
        _WholeBodyCocoTopDownDataset.__init__(self, *args, **kwargs)
