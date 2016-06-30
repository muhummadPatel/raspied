from pipeline.storage import PipelineMixin
from whitenoise.django import GzipManifestStaticFilesStorage


class GzipManifestPipelineStorage(PipelineMixin, GzipManifestStaticFilesStorage):
    # hybrid storage class with mixins from pipeline and whitenoise so they
    # play nicely. See STATICFILES_STORAGE in settings.py, and pipeline docs
    # about using pipeline with other storage solutions.
    pass
