   
from django.urls import path,include
from api.viewsfolder.notification_views import savenotification,sendnotificationforexcelsheet,notificationDataGrid,notificationDataGridChild,saveExcelData,importExcelfunc


urlpatterns=[ 
    path('savenotification/',savenotification,name='savenotification'),
    path('sendnotificationforexcelsheet/',sendnotificationforexcelsheet,name='sendnotificationforexcelsheet'),
    path('notificationdatagrid/',notificationDataGrid,name='notificationDataGrid'),
    path('notificationdatagridchild/',notificationDataGridChild,name='notificationDataGridChild'),
    path('saveexceldata/',saveExcelData,name='saveExcelData'),
    path('importexcel/',importExcelfunc,name='iportExcelfunc'),
    ]