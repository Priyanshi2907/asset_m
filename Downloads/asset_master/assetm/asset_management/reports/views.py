from django.shortcuts import render
from asset_master.models import *
from requirements.models import *
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from repair_maintenance.models import *
from orders.models import *
from django.http import HttpResponse, JsonResponse
import csv
import datetime
from django.db.models import Q






# Create your views here.
def asset_report_main_page(request):
    return render(request, 'asset_report_main_page.html')



def asset_report_order_analysis(request):
    ctx={}
    all_orders = OrderDetail.objects.all().values("id","organization",
                                                  "out_date_and_time",
                                                  "deployment_date", "return_date")
    ctx['all_orders'] = all_orders

    return render(request, 'asset_order_report_table.html', ctx)



#Asset Ongoing orders...
def asset_report_ongoing_orders(request):
    ctx={}
    today = datetime.date.today()
    order_dispatch = OrderDetail.objects.filter(order_dispatch=True,
                                                return_date__gte=today).values("id","organization",
                                                  "out_date_and_time",
                                                  "deployment_date", "return_date")
    
    ctx['all_orders'] = order_dispatch

    return render(request, 'asset_ongoing_orders.html', ctx)



#Asset Report completed orders...
def asset_report_completed_orders(request):
    # return_after_one_day = datetime.datetime.now() - datetime.timedelta(days=1)
    today = datetime.date.today()
    
    ctx={}
    order_completed = OrderDetail.objects.filter(order_dispatch=True,
                                                return_date__lt=today
                                                ).values("id",
                                                    "organization",
                                                    "out_date_and_time",
                                                    "deployment_date",
                                                    "return_date"
                                                  )
    
    ctx['order_completed'] = order_completed

    return render(request, 'asset_report_completed_orders.html', ctx)



#Asset Report of booked orders...
def asset_report_booked_orders(request):
    return_after_one_day = datetime.datetime.now() - datetime.timedelta(days=1)
    
    ctx={}
    order_booked_status = OrderDetail.objects.filter(
                                                Q(order_status=1) |
                                                Q(order_status=2),
                                                order_dispatch=False,
                                                ).values("id",
                                                    "organization",
                                                    "out_date_and_time",
                                                    "deployment_date",
                                                    "return_date"
                                                  )
    
    ctx['order_booked_status'] = order_booked_status

    return render(request, 'asset_report_booked_orders.html', ctx)



#Asset allocated to order...
def asset_allocated_to_orders(request, id):
    
    
    ctx={}
    order_booked_status = list(OrderDetail.objects.filter(id=id
                                                ).values("id",
                                                    "organization",
                                                    "out_date_and_time",
                                                    "deployment_date",
                                                    "return_date",
                                                    "assets__id",
                                                    "assets__relation",
                                                    "assets__mapping",
                                                    "assets__description",
                                                    "assets__model_no",
                                                    "assets__serial_no",
                                                    "assets__brand",
                                                    "assets__category"
                                                ))
    parent_assets = []
    child_assets = []
    for asset in order_booked_status:
        if asset['assets__relation'] == 101:
            parent_assets.append(asset)
        else:
            child_assets.append(asset)

    for asset in parent_assets:
        if 'asset_accessories' not in asset:
            asset['asset_accessories'] = []
            asset['asset_accessories_description'] = []
     
        for asset_acc in child_assets:
            if asset_acc['assets__mapping'] == asset['assets__description']:
                if (asset_acc['assets__description']) not in asset['asset_accessories_description']: 
                    asset['asset_accessories_description'].append(asset_acc['assets__description'])
                    asset['asset_accessories'].append({
                        'description': asset_acc['assets__description'],
                        'id':asset_acc['assets__id'],
                        'serial_no':asset_acc['assets__serial_no'],
                        'model_no':asset_acc['assets__model_no'],
                        'brand':asset_acc['assets__brand']
                    })
                    child_assets.remove(asset_acc)


    paginator = Paginator(parent_assets, 10) 
    page = request.GET.get('page')

    try:
        asset_obj_paginated = paginator.page(page)
    except PageNotAnInteger:

        asset_obj_paginated = paginator.page(1)
    except EmptyPage:

        asset_obj_paginated = paginator.page(paginator.num_pages)

    ctx["asset_obj"] = asset_obj_paginated
    ctx['order_booked_status'] = order_booked_status

    return render(request, 'asset_allocated_to_orders.html', ctx)





def asset_reports_table(request):
    availability_list = []
    out_list = []
    all_data = []
    ctx = {}
    page_number = request.GET.get('page', 1) 
    query_params_q = request.GET.get('q')
    query_params_filter_value = request.GET.get('filter_type')

    if query_params_q and query_params_filter_value == 'category':
        categories_with_total_asset_count = AssetMaster.objects.filter(category__iexact=query_params_q,sold_asset=False).values('category').annotate(category_count=Count('category'))
    else:
        categories_with_total_asset_count = AssetMaster.objects.filter(sold_asset=False).values('category').annotate(category_count=Count('category'))

    dispatched_status = OrderDetail.OrderStatus.DISPATCHED

    for i in categories_with_total_asset_count:
        category_name = i['category']
        
        total_count = i['category_count']
        
        # # Count assets that are available
        # categories_with_availability_count1 = AssetMaster.objects.filter(
        #     category=category_name,
        #     add_to_order=True,
        #     confirm_order=False
        # ).count()

        # categories_with_availability_count2 = AssetMaster.objects.filter(
        #     category=category_name,
        #     asset_status__in=['available']
        # ).count()

        # availability_count = categories_with_availability_count1 + categories_with_availability_count2
        
       # Count assets that are dispatched and not moved to inventory
        dispatched_assets = OrderDetail.objects.filter(
            order_status=dispatched_status,
            assets__category=category_name,
            assets__add_to_order=True,
            assets__confirm_order=True,
            assets__assetmasterinventory__move_to_inventory=False
        )

        dispatched_count = dispatched_assets.count()

        # Count assets that are sent for repair
        sent_for_repair_count = AssetMaster.objects.filter(
            category=category_name,
            asset_status='sent_for_repair'
        ).count()

         # Count assets that are rented out but not dispatched
        rented_out_count = AssetMaster.objects.filter(
            category=category_name,
            asset_status='rented_out',
            add_to_order=True,
            confirm_order=True
            
        ).exclude(id__in=dispatched_assets.values_list('assets__id',flat=True)).count()
 
        sold_count=AssetMaster.objects.filter(
            category=category_name,
            sold_asset=True           
        ).count()
        # Calculate availability as total_count minus dispatched_count and rented_out_count
        availability_count = total_count - (dispatched_count + rented_out_count)

        availability_dict = {'availability': availability_count}
        out_dict = {'out': total_count - availability_count}
        
        all_data.append({
            'category': category_name,
            'category_count': total_count,
            'availability': availability_count,
            'dispatched_count': dispatched_count,
            'sent_for_repair_count': sent_for_repair_count,
            'rented_out_count': rented_out_count,
            'sold_count':sold_count,
            'out': total_count - availability_count
        })

    paginator = Paginator(all_data, 10) 
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)

    ctx['category_list'] = paginated_data
    ctx['query_params_q'] = query_params_q
    ctx['query_params_filter_value'] = query_params_filter_value
    ctx['queryset_length'] = len(all_data)

    download_csv_param = request.GET.get('download_csv')
    if download_csv_param:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Asset Report(Category wise).csv"'

        # Write data to CSV
        writer = csv.writer(response)
        writer.writerow(['Category', 'Category Count', 'Availability', 'Out']) 
        for item in all_data:
            writer.writerow([item['category'], item['category_count'], item['availability'], item['out']])

        return response

    return render(request, 'assets_report_table.html',ctx)




# Each Category brand table
def each_category_brand_report(request, category):
    ctx = {}
    availability_list = []
    all_data = []
    brand_non_availability_list = []
    page_number = request.GET.get('page', 1)
    request.session['category'] = category

    query_params_q = request.GET.get('q')
    query_params_filter_value = request.GET.get('filter_type')

    if query_params_q:
        category_brand = AssetMaster.objects.filter(category__iexact=category, brand=query_params_q,sold_asset=False).values('brand','category').annotate(brand_count=Count('brand'))
    else:
        category_brand = AssetMaster.objects.filter(category__iexact=category,sold_asset=False).values('brand','category').annotate(brand_count=Count('brand'))

    brand_length = len(category_brand)
    dispatched_status = OrderDetail.OrderStatus.DISPATCHED

    for i in category_brand:
        category_name=i['category']
        brand_name = i['brand']
        
        
        # Count assets that are dispatched and not moved to inventory
        dispatched_assets = OrderDetail.objects.filter(
            order_status=dispatched_status,
            assets__category=category,
            assets__brand=brand_name,
            assets__add_to_order=True,
            assets__confirm_order=True,
            assets__assetmasterinventory__move_to_inventory=False
        )

        dispatched_count = dispatched_assets.count()
        
        # Count assets that are sent for repair
        sent_for_repair_count = AssetMaster.objects.filter(
            category=category,
            brand=brand_name,
            asset_status='sent_for_repair'
        ).count()

        # Count assets that are rented out but not dispatched
        rented_out_count = AssetMaster.objects.filter(
            category=category_name,
            brand=brand_name,
            asset_status='rented_out',
            add_to_order=True,
            confirm_order=True
            
        ).exclude(id__in=dispatched_assets.values_list('assets__id',flat=True)).count()

        sold_count=AssetMaster.objects.filter(
            category=category_name,
            brand=brand_name,
            sold_asset=True           
        ).count()
        # Calculate availability as total_count minus dispatched_count and rented_out_count
        availability_count = i['brand_count'] - (dispatched_count + rented_out_count)

        availability_dict = {'availability': availability_count}
        out_dict = {'not_available': i['brand_count'] - availability_count}
        
        all_data.append({
            'category': category_name,
            'brand': brand_name,
            'brand_count': i['brand_count'],
            'availability': availability_count,
            'dispatched_count': dispatched_count,
            'sent_for_repair_count': sent_for_repair_count,
            'rented_out_count': rented_out_count,
            'sold_count':sold_count,
            'not_available': i['brand_count'] - availability_count
        })

    if query_params_filter_value:
        ctx['query_params_filter_value'] = query_params_filter_value
    if query_params_q:
        ctx['query_params_q'] = query_params_q

    # Pagination
    paginator = Paginator(all_data, 10)
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)

    ctx['category_brand'] = paginated_data
    ctx['category'] = category
    ctx['brand_length'] = brand_length
    ctx['queryset_length'] = len(all_data)

    download_csv_param = request.GET.get('download_csv')
    if download_csv_param:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

        # Write data to CSV
        writer = csv.writer(response)
        writer.writerow(['Brand', 'Brand Count', 'Availability']) 
        for item in all_data:
            writer.writerow([item['brand'], item['brand_count'], item['availability']])

        return response
    
    
    return render(request,'asset_report_brand_list.html',ctx)




#Each brand model no.
def each_brand_model_no_report(request, brand):
    ctx = {}
    availability_list = []
    all_data = []
    model_non_availability_list = []
    page_number = request.GET.get('page', 1)
    #request.session['category'] = category
    category=request.session['category']
    #request.session['brand'] = brand

    query_params_q = request.GET.get('q')
    query_params_filter_value = request.GET.get('filter_type')

    if query_params_q:
        category_brand_model = AssetMaster.objects.filter(
            category=category,
            brand=brand,
            model_no__iexact=query_params_q,
            sold_asset=False
        ).values('model_no', 'category', 'brand').annotate(model_count=Count('model_no'))
    else:
        category_brand_model = AssetMaster.objects.filter(
            category=category,
            brand=brand,
            sold_asset=False
        ).values('model_no', 'category', 'brand').annotate(model_count=Count('model_no'))

    model_length = len(category_brand_model)
    dispatched_status = OrderDetail.OrderStatus.DISPATCHED

    for i in category_brand_model:
        category_name = i['category']
        brand_name = i['brand']
        model_no = i['model_no']
        total_count = i['model_count']

        # Count assets that are dispatched and not moved to inventory
        dispatched_assets = OrderDetail.objects.filter(
            order_status=dispatched_status,
            assets__category=category,
            assets__brand=brand,
            assets__model_no=model_no,
            assets__assetmasterinventory__move_to_inventory=False
        )

        dispatched_count = dispatched_assets.count()

        # Count assets that are rented out but not dispatched
        rented_out_assets = AssetMaster.objects.filter(
            category=category,
            brand=brand,
            model_no=model_no,
            add_to_order=True,
            confirm_order=True
        ).exclude(id__in=dispatched_assets.values_list('assets__id', flat=True))

        rented_out_count = rented_out_assets.count()

        # Count assets that are sent for repair
        sent_for_repair_count = AssetMaster.objects.filter(
            category=category,
            brand=brand,
            model_no=model_no,
            asset_status='sent_for_repair'
        ).count()

        sold_count=AssetMaster.objects.filter(
            category=category,
            brand=brand,
            model_no=model_no,
            sold_asset=True
        ).count()
        # Calculate availability as total_count minus dispatched_count and rented_out_count
        availability_count = total_count - dispatched_count - rented_out_count

        all_data.append({
            'category': category_name,
            'brand': brand_name,
            'model_no': model_no,
            'model_count': total_count,
            'availability': availability_count,
            'dispatched_count': dispatched_count,
            'sent_for_repair_count': sent_for_repair_count,
            'rented_out_count': rented_out_count,
            'sold_count':sold_count,
            'not_available': total_count - availability_count
        })

    if query_params_filter_value:
        ctx['query_params_filter_value'] = query_params_filter_value
    if query_params_q:
        ctx['query_params_q'] = query_params_q

    # Pagination
    paginator = Paginator(all_data, 10)
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)

    ctx['category_brand_model'] = paginated_data
    ctx['category'] = category
    ctx['brand'] = brand
    ctx['model_length'] = model_length
    ctx['queryset_length'] = len(all_data)
    download_csv_param = request.GET.get('download_csv')
    if download_csv_param:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

        # Write data to CSV
        writer = csv.writer(response)
        writer.writerow(['Model No.', 'Model Count', 'Availability']) 
        for item in all_data:
            writer.writerow([item['model_no'], item['model_count'], item['availability']])

        return response
    return render(request,'asset_report_model_list.html',ctx)







#Asset report of repair
def asset_report_of_repair(request, category):
    ctx={}
    asset_master_category = list(AssetMaster.objects.filter(category=category,
                                                        asset_status='sent_for_repair'
                                                        ).values_list('id'))
    asset_id_list = [m[0] for m in asset_master_category]
    internal_repair_count = list(InternalRepairAndMaintenance.objects.filter(
        asset_obj__id__in=asset_id_list).values('equipment_handing_over_date',
                                                 'equipment_received_date',
                                                 'asset_obj__description'))
    repair_type='Interal Repair'
    for i in internal_repair_count:
        i['repair_type'] = repair_type
        i['category'] = category
    external_repair_count = list(ExternalRepairAndMaintenance.objects.filter(
        asset_obj__id__in=asset_id_list).values('date_of_collection',
                                                 'date_of_receipt',
                                                 'asset_obj__description'))
    repair_type='Exteral Repair'
    for i in external_repair_count:
        i['repair_type'] = repair_type
        i['category'] = category
    ctx['internal_repair_list'] =  internal_repair_count
    ctx['external_repair_list'] =  external_repair_count
    
    
    download_csv_param = request.GET.get('download_csv')
    if download_csv_param:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Asset Report(Internal maintenance).csv"'

        # Write data to CSV
        writer = csv.writer(response)
        writer.writerow(['Category', 'equipment_handing_over_date', 'equipment_handing_over_date']) 
        for item in internal_repair_count:
            writer.writerow([category, item['equipment_handing_over_date'], item['equipment_handing_over_date']])

        return response
    return render(request, 'asset_report_of_repair.html', ctx)




#Category wise rented out details
def category_wise_rented_out_details(request, category):
    ctx = {}
    asset_master_category = list(AssetMaster.objects.filter(category=category,
                                                        asset_status='rented_out',
                                                        confirm_order=True
                                                        ).values_list('id'))
    asset_id_list = [m[0] for m in asset_master_category]

    all_orders_list = list(OrderDetail.objects.filter(assets__id__in=asset_id_list).values('id','organization',
                                                                                    'out_date_and_time',
                                                                                    'return_date',
                                                                                    'assets__description',
                                                                                    'assets__brand'))
    for i in all_orders_list:
        i['category'] = category
    
    ctx['all_orders_list'] = all_orders_list
    
    return render(request, 'rented_out_details.html', ctx)




#Model No. wise rented out details
def model_no_wise_rented_out_details(request, model_no):
    category=request.session['category']
    brand=request.session['brand']
    model_no=request.session['model_no']

    ctx = {}
    asset_master_category = list(AssetMaster.objects.filter(category=category,
                                                        brand=brand,
                                                        model_no=model_no,
                                                        asset_status='rented_out',
                                                        confirm_order=True
                                                        ).values_list('id'))
    asset_id_list = [m[0] for m in asset_master_category]

    all_orders_list = list(OrderDetail.objects.filter(assets__id__in=asset_id_list).values('id','organization',
                                                                                    'out_date_and_time',
                                                                                    'return_date',
                                                                                    'assets__description',
                                                                                    'assets__brand'))
    for i in all_orders_list:
        i['category'] = category
    
    ctx['all_orders_list'] = all_orders_list
    
    return render(request, 'rented_out_details.html', ctx)




#Category wise repair and maintenance
def category_wise_repair_and_maintenance(request, category):
    ctx = {}
    sent_for_repair_category_wise = list(AssetMaster.objects.filter(category=category,
                                                        asset_status='sent_for_repair'
                                                        ).values_list('id'))
    
    asset_id_list = [m[0] for m in sent_for_repair_category_wise]

    all_orders_list = list(OrderDetail.objects.filter(assets__id__in=asset_id_list).values('id','organization',
                                                                                    'out_date_and_time',
                                                                                    'return_date'))
    for i in all_orders_list:
        i['category'] = category
    
    ctx['all_orders_list'] = all_orders_list
    
    return render(request, 'rented_out_details.html', ctx)






def asset_report_out_list(request,category):
    ctx={}
    asset_master_category_rented = AssetMaster.objects.filter(category=category,
                                                                asset_status='rented_out',
                                                                confirm_order=True
                                                                ).count()
    
    asset_master_sent_for_repair = AssetMaster.objects.filter(category=category,
                                                        asset_status='sent_for_repair'
                                                        ).count()
    
    ctx['asset_master_category_rented'] = asset_master_category_rented
    ctx['asset_master_sent_for_repair'] = asset_master_sent_for_repair
    ctx['category'] = category

    return render(request, 'asset_report_out_list.html', ctx)





#Asset report of repair
def asset_report_out_list_brand_wise(request, brand):
    ctx={}
    category=request.session['category']
    asset_master_category_rented = AssetMaster.objects.filter(category=category,
                                                                brand=brand,
                                                                asset_status='rented_out',
                                                                confirm_order=True
                                                                ).count()
    
    asset_master_sent_for_repair = AssetMaster.objects.filter(category=category,
                                                                brand=brand,
                                                                asset_status='sent_for_repair'
                                                        ).count()
    
    ctx['asset_master_category_rented'] = asset_master_category_rented
    ctx['asset_master_sent_for_repair'] = asset_master_sent_for_repair
    ctx['category'] = category
    ctx['brand'] = brand
    return render(request, 'asset_report_out_list_brand_wise.html', ctx)




#Asset report of repair
def asset_report_out_list_model_no_wise(request, model_no):
    ctx={}
    category=request.session['category']
    brand=request.session['brand']
    request.session['model_no'] = model_no

    asset_master_category_rented = AssetMaster.objects.filter(category=category,
                                                                brand=brand,
                                                                model_no=model_no,
                                                                asset_status='rented_out',
                                                                confirm_order=True
                                                                ).count()
    
    asset_master_sent_for_repair = AssetMaster.objects.filter(category=category,
                                                                brand=brand,
                                                                model_no=model_no,
                                                                asset_status='sent_for_repair'
                                                        ).count()
    
    ctx['asset_master_category_rented'] = asset_master_category_rented
    ctx['asset_master_sent_for_repair'] = asset_master_sent_for_repair
    ctx['category'] = category
    ctx['brand'] = brand
    return render(request, 'asset_report_out_list_model_no_wise.html', ctx)





#Category wise rented out details
def category_brand_wise_rented_out_details(request, brand):
    ctx = {}
    category=request.session['category']
    asset_master_category = list(AssetMaster.objects.filter(category=category,
                                                            brand=brand,
                                                            asset_status='rented_out',
                                                            confirm_order=True
                                                        ).values_list('id'))
    asset_id_list = [m[0] for m in asset_master_category]

    all_orders_list = list(OrderDetail.objects.filter(assets__id__in=asset_id_list).values('id','organization',
                                                                                    'out_date_and_time',
                                                                                    'return_date',
                                                                                    'assets__description'))
    for i in all_orders_list:
        i['category'] = category
    
    ctx['all_orders_list'] = all_orders_list
    ctx['brand'] = brand
    
    return render(request, 'category_brand_wise_list.html', ctx)




#Asset report of repair
def asset_report_of_repair_category_brand_wise(request, brand):
    ctx={}
    category=request.session['category']
    asset_master_category = list(AssetMaster.objects.filter(category=category,
                                                        brand=brand,
                                                        asset_status='sent_for_repair'
                                                        ).values_list('id'))
    asset_id_list = [m[0] for m in asset_master_category]
    internal_repair_count = list(InternalRepairAndMaintenance.objects.filter(
        asset_obj__id__in=asset_id_list).values('equipment_handing_over_date',
                                                 'equipment_received_date',
                                                 'asset_obj__description'))
    repair_type='Interal Repair'
    for i in internal_repair_count:
        i['repair_type'] = repair_type
        i['category'] = category
    external_repair_count = list(ExternalRepairAndMaintenance.objects.filter(
        asset_obj__id__in=asset_id_list).values('date_of_collection',
                                                 'date_of_receipt',
                                                 'asset_obj__description'))
    repair_type='Exteral Repair'
    for i in external_repair_count:
        i['repair_type'] = repair_type
        i['category'] = category
    ctx['internal_repair_list'] =  internal_repair_count
    ctx['external_repair_list'] =  external_repair_count



    download_csv_param = request.GET.get('download_csv')
    if download_csv_param:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Asset Report(Internal maintenance).csv"'

        # Write data to CSV
        writer = csv.writer(response)
        writer.writerow(['Category', 'equipment_handing_over_date', 'equipment_handing_over_date']) 
        for item in internal_repair_count:
            writer.writerow([category, item['equipment_handing_over_date'], item['equipment_handing_over_date']])

        return response

    return render(request, 'asset_report_of_repair.html', ctx)
##############################
# Access report list
def excess_report_list(request):
    availability_list = []
    out_list = []
    all_data = []
    merged_data=[]
    #for order id
    # customer_orders = CustomerDetail.objects.filter(id=id).values('orderdetail__id',
    # 'customer', 'orderdetail__price', 'orderdetail__deployment_date',
    # 'orderdetail__return_date', 'orderdetail__order_status', 'orderdetail__order_dispatch')

    
    # all_asset_of_an_order = OrderDetail.objects.values('assets__id','assets__box_number',
    # 'assets__category', 'assets__description', 'assets__brand', 'assets__serial_no', 'assets__model_no', 
    # 'assets__owner', 'assets__sub_category', 'order_dispatch', 'approve_order'
    # )
    # print(all_asset_of_an_order)
   
    # asset_count=OrderDetail.objects.filter().values('assets__category').annotate(Count='assets__category')
    # print(asset_count)
    Requiremnt_asset=RequirementDetail.objects.values('id','r_category','r_description','r_serialno',
                                'r_modelno', 'r_brand' )
    asset_count=OrderDetail.objects.values('assets__category').annotate(count=Count('assets__category'))
    requirement_count=RequirementDetail.objects.values('id').annotate(total=Count('id'))
    order=OrderDetail.objects.all().order_by('-id')
    # for m in order:
    #     all_asset_of_an_order=OrderDetail.objects.filter(id=m['id']).values('assets__id',  'assets__category',
    #                                                                          'assets__description', 'assets__brand', 'assets__serial_no', 'assets__model_no')
    #     asset_count=all_asset_of_an_order.count()
    orders=OrderDetail.objects.values('id').annotate(asset_count=Count('assets__id'))
    req=RequirementDetail.objects.values('id')
    #     print(asset_count)
    #     for r in Requiremnt_asset:
    #         if m['assets__category']== r['r_category']:
    #              merged_data.append({
    #                  **{"req_count":r['quantity']},
    #                 **{'orders':orders}})
   
    ctx={'order':order}
       
  
    
         
        #   }
    
    # print(asset_count.count)
    asset_obj = AssetMaster.objects.filter(
            sold_asset=False,
            confirm_order=False,
            add_to_order=True, 
            relation=101
            ).values('id','category','description','serial_no',
                                'model_no', 'brand', 'add_to_order')
    
    Requiremnt_asset=RequirementDetail.objects.values('id','r_category','r_description','r_serialno',
                                'r_modelno', 'r_brand')
    categories_count= AssetMaster.objects.values('category').annotate(category_count=Count('category'))
    
    # for m in categories_count:
    #    for r in  Requiremnt_asset:
    #        if (m["category"] == r["r_category"]) :
    #            merged_data.append({
    #                **{'category':m['category']}, 
    #                **{'cat_count':m['category_count']},
    #                **{'req_count':r['quantity']},
    #                **{'excess':m['category_count']-r['quantity'] if m['category_count']>r['quantity'] else "--"},
    #                **{'shortfall':r['quantity']-m['category_count'] if r['quantity']>m['category_count'] else "--"}})
               
        # req_count = requirement_count.filter(r_category=m['category']).order_by(
        #     'r_category')
        # if req_count:
        #     excess=m['category_count']-req_count['quantity']
        #     merged_data.append({**{'category':m['category']}, **{'cat_count':m['category_count']},**{'req_count':req_count[requirement_count]},**{'excess':excess if excess >0 else 0,}})
        # else:
        #     merged_data.append({**{'category':m['category']}, **{'cat_count':m['category_count']},**{'req_count':0},**{'excess':m['category_count']}})
    
    return render(request,'excess_report_list.html',ctx )

    # for i in categories_with_total_asset_count:
    #     categories_with_availability_count1 = AssetMaster.objects.filter(category=i['category'],
    #                                                                   add_to_order=True,
    #                                                                   confirm_order=False,
    #                                                                   ).count()
    #     categories_with_availability_count2 = AssetMaster.objects.filter(category=i['category'],
    #                                                                   asset_status__in =['available']
    #                                                                   ).count()
    #     availability_dict = {'availability': (categories_with_availability_count1 + categories_with_availability_count2)}
    #     availability_list.append(availability_dict)
    #     categories_with_total_asset_count_dict = list(categories_with_total_asset_count.values('category', 'category_count'))
    #     categories_with_total_asset_count_dict = list(categories_with_total_asset_count.values('category', 'category_count'))
    #     for i, j in  zip(categories_with_total_asset_count_dict, availability_list):
    #          all_data.append({**i, **j, })
    
    #     ctx['cusobj']= categories_with_total_asset_count_dict
    # if(RequirementDetail.r_category==AssetMaster.category):

    # page_number = request.GET.get('page', 1) 
    # if request.GET.get('q') and request.GET.get('filter_type') == 'category':
    #     category=request.GET.get('q')
    #     categories_with_total_asset_count = AssetMaster.objects.filter(category__iexact=category).values('category').annotate(category_count=Count('category'))
    # else:
    #     categories_with_total_asset_count = AssetMaster.objects.values('category').annotate(category_count=Count('category'))
    # for i in categories_with_total_asset_count:
    #     categories_with_availability_count1 = AssetMaster.objects.filter(category=i['category'],
    #                                                                   add_to_order=True,
    #                                                                   confirm_order=False,
    #                                                                   ).count()
    #     categories_with_availability_count2 = AssetMaster.objects.filter(category=i['category'],
    #                                                                   asset_status__in =['available']
    #                                                                   ).count()
    #     availability_dict = {'availability': (categories_with_availability_count1 + categories_with_availability_count2)}
    #     availability_list.append(availability_dict)

    #     # out_dict = {'out': i['category_count'] -
    #     #             (categories_with_availability_count1 + categories_with_availability_count2)}
    #     # out_list.append(out_dict)
    # categories_with_total_asset_count_dict = list(categories_with_total_asset_count.values('category', 'category_count'))
    # for i, j, k in  zip(categories_with_total_asset_count_dict, availability_list, out_list):
    #     all_data.append({**i, **j, **k})

    # paginator = Paginator(all_data, 10) 
    # try:
    #     paginated_data = paginator.page(page_number)
    # except PageNotAnInteger:
    #     paginated_data = paginator.page(1)
    # except EmptyPage:
    #     paginated_data = paginator.page(paginator.num_pages)

    # ctx['category_list'] = paginated_data
    download_csv_param = request.GET.get('download_csv')
    if download_csv_param:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Asset Report(Category wise).csv"'

    #     # Write data to CSV
    #     writer = csv.writer(response)
    #     writer.writerow(['Category', 'Category Count', 'Availability', 'Out']) 
    #     for item in all_data:
    #         writer.writerow([item['category'], item['category_count'], item['availability'], item['out']])

    #     return response

    # return render(request,"excess_report_list.html",ctx)

def excess_shortfall(request,id):
    merged_data=[]
    ctx={}
    order_info = OrderDetail.objects.filter(id=id).all()
    rcust = RequirementCust.objects.filter(id=order_info[0].req_id.id).values('r_cust_id')
    rcust_id = rcust[0]['r_cust_id']
    requirement_category = RequirementDetail.objects.filter(r_unique_id=rcust_id).values('r_category','r_description').distinct().annotate(req_count=Count('r_category'))
    order_category = OrderDetail.objects.filter(id=id).values('assets__category','assets__description').distinct().annotate(category_count=Count('assets__category'))
    print("order: ",order_category)
    print("requiremnt: ",requirement_category)
    
    for m in order_category:
        for r in requirement_category:
            if m['assets__category'] == r['r_category'] and m['assets__description']==r['r_description']:
             merged_data.append({
                    **{'category':m['assets__category']}, 
                    **{'cat_count':m['category_count']},
                    **{'req_count':r['req_count']},
                    **{'excess':m['category_count']-r['req_count'] if m['category_count']>r['req_count'] else "--"},
                    **{'shortfall':r['req_count']-m['category_count'] if r['req_count']>m['category_count'] else "--"}
            })
            
        # else:
        #      merged_data.append({
        #         **{'category': m['assets__category']},
        #         **{'cat_count': m['category_count']},
        #         **{'req_count': 0},
        #         **{'excess': 0},
        #         **{'shortfall': 0}
        #     })
    

                
               
    # print(order_category)   
    # print(requirement_category)
    ctx['order_info']=order_info
    ctx['order_category']=order_category
    ctx['merged_data']=merged_data
    return render(request,'excess_shortfall.html',ctx)