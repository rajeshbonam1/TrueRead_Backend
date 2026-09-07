from django.urls import path
from api import views


urlpatterns = [

    # ============================================================
    # USER MANAGEMENT
    # ============================================================

    # User / Meter Reader registration
    path(
        'register/',
        views.meterReaderRegistrationfun,
        name='register'
    ),

    path(
        'registerupdate/',
        views.meterReaderRegistrationUpdateOffice,
        name='registerupdate'
    ),

    # Login
    path(
        'login/',
        views.metereReaderlogin,
        name='login'
    ),

    path(
        'loginuser/',
        views.loginuser,
        name='loginuser'
    ),

    # Office / hierarchy data
    path(
        'officejson/',
        views.get_officedata,
        name='officejson'
    ),

    path(
        'discom/',
        views.get_discom,
        name='discom'
    ),

    path(
        'zone/',
        views.get_zone,
        name='zone'
    ),

    path(
        'circle/',
        views.get_circle,
        name='circle'
    ),

    path(
        'division/',
        views.get_division,
        name='division'
    ),

    path(
        'subdivision/',
        views.get_subdivision,
        name='subdivision'
    ),

    path(
        'section/',
        views.get_section,
        name='section'
    ),

    path(
        'sectionuser/',
        views.get_sectionforuser,
        name='sectionuser'
    ),


    # ============================================================
    # FIELD FORCE
    # ============================================================

    # Consumer data
    path(
        'consumers/',
        views.consumers,
        name='consumers'
    ),

    path(
        'getconsumers/',
        views.getconsumers,
        name='getconsumers'
    ),

    path(
        'getconsumerscount/',
        views.getconsumerscount,
        name='getconsumerscount'
    ),

    path(
        'consdetails/',
        views.consdetail,
        name='consdetails'
    ),

    # Meter Reader data
    path(
        'getregdata/',
        views.getregdata,
        name='getregdata'
    ),

    path(
        'getmridforsection/',
        views.getmridforSection,
        name='getmridforsection'
    ),

    path(
        'meterreaderdetail/',
        views.get_meter_reader_detail,
        name='meterreaderdetail'
    ),

    path(
        'newmeterreaderdetails/',
        views.meterreaderDetails,
        name='meterreaderdetails'
    ),

    path(
        'get_mr_subdiv/',
        views.get_meter_reader_subdivision,
        name='meter-reader-subdivision'
    ),

    # Map / cluster APIs
    path(
        'clusters/',
        views.clusters,
        name='clusters'
    ),

    path(
        'clusterstest/',
        views.clusterstest,
        name='clusterstest'
    ),

    path(
        'clusterstestnew/',
        views.clusterstestnew,
        name='clusterstestnew'
    ),

    path(
        'geocluster/',
        views.geocluster,
        name='geocluster'
    ),

    path(
        'geoclusternew/',
        views.geoclusternew,
        name='geoclusternew'
    ),

    path(
        'consumerwisemap/',
        views.consumerwisemap,
        name='consumerwisemap'
    ),

    # Supervisor
    path(
        'supervisorlogin/',
        views.supervisorlogin,
        name='supervisorlogin'
    ),

    path(
        'supervisorlocation/',
        views.supervisorlocation,
        name='supervisorlocation'
    ),

]