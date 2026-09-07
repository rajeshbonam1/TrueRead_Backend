@api_view(['GET',])
def mvcheck(request):
    pagesize = request.query_params.get("pagesize",)
    paginator = PageNumberPagination()
    paginator.page_size = pagesize
    monthByData = request.query_params.get("getMonth", None)
    orderby = request.query_params.get("orderby", None)
    mrid = request.query_params.get('mrid', None)
    startDate = request.query_params.get('startdate', None)
    endDate = request.query_params.get('enddate', None)
    endDate = request.query_params.get('enddate', None)
    searchdata = request.query_params.get('searchdata', None)
    clause = ''
    if monthByData:
        monthByData = monthByData.split('-')[1]
        print("month--after---------", monthByData)
        clause = f"where EXTRACT(MONTH FROM m.reading_date_db)='{monthByData}'"

    elif startDate and endDate:
        clause = f"where m.reading_date_db BETWEEN {startDate} AND {endDate}"
        
    elif mrid:
        clause = f"where m.mr_id='{mrid}'"
        
    elif searchdata:
        clause = f"where m.mr_id='{searchdata}'"
        print(clause)
    else:
        clause = ''
    query=Consumers.objects.raw(f'''select m.mr_id as "mrId",m.rdng_date,m.prsnt_mtr_status,m.prsnt_ocr_rdng,m.prsnt_rdng,m.ocr_pf_reading,m.cons_name,m.prsnt_md_rdng_ocr,m.rdng_ocr_status,m.rdng_img,m.prsnt_md_rdng,m.id,r."mrPhoto"
                    from readingmaster m left outer join meterreaderregistration r on m.mr_id=r."mrId" {clause} order by m.rdng_date {orderby} 

    ''')
    print(query)
    serializer=ConsumersMeterRegistration(query,many=True)
    result_page = paginator.paginate_queryset(serializer.data, request)
    return paginator.get_paginated_response(result_page)