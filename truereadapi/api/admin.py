from django.contrib import admin
from .models import (
    Abnormality,
    Agency,
    ImageCheck,
    MeterPhase,
    MeterStatus,
    OcrException,
    OcrStatus,
    Office,
    MeterReader,
    MeterReading,
    MeterReadingDetail,
    OcrOverride,
)


admin.site.register(Abnormality)
admin.site.register(Agency)
admin.site.register(ImageCheck)
admin.site.register(MeterPhase)
admin.site.register(MeterStatus)
admin.site.register(OcrException)
admin.site.register(OcrStatus)
admin.site.register(Office)
admin.site.register(MeterReader)
admin.site.register(MeterReading)
admin.site.register(MeterReadingDetail)
admin.site.register(OcrOverride)