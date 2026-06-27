from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import qrcode
from io import BytesIO
from django.core.files import File
from .models import QRCode
from django.http import HttpResponseRedirect

# Create your views here.

@login_required
def dashboard(request):

    recent_qrs = QRCode.objects.filter(
        user=request.user
    ).order_by('-created_at')[:3]

    if request.method == 'POST':

        total = QRCode.objects.filter(
            user=request.user
        ).count()

        
        if total >= 10:
            return render(
                request,
                'dashboard.html',
                {
                    'error': 'You can generate only 10 QR codes.',
                    'recent_qrs': recent_qrs,
                }
            )

        url = request.POST.get('url')

        qr_obj = QRCode.objects.create(
            user=request.user,
            url=url
        )

        track_url = request.build_absolute_uri(
        f'http://172.27.87.9:8000/scan/{qr_obj.id}/'
        )

        qr = qrcode.make(track_url)

        buffer = BytesIO()
        qr.save(buffer)



        file_name = f'qr_{request.user.id}_{total + 1}.png'

        qr_obj.qr_image.save(
            file_name,
            File(buffer),
            save=True
        )

        return redirect('my_qrs')

    return render(
        request,
        'dashboard.html',
        {
            'recent_qrs': recent_qrs,
        }
    )


@login_required
def my_qrs(request):

    query = request.GET.get('q')
    status = request.GET.get('status')

    qrs = QRCode.objects.filter(
        user=request.user
    ).order_by('-created_at')

   
    if query:
        qrs = qrs.filter(
            url__icontains=query
        )

    
    if status == 'active':
        qrs = qrs.filter(
            is_active=True
        )

    elif status == 'paused':
        qrs = qrs.filter(
            is_active=False
        )

    total_qrs = QRCode.objects.filter(
        user=request.user
    ).count()

    active_qrs = QRCode.objects.filter(
        user=request.user,
        is_active=True
    ).count()

    paused_qrs = QRCode.objects.filter(
        user=request.user,
        is_active=False
    ).count()

    return render(
        request,
        'qrapp/my_qrs.html',
        {
            'qrs': qrs,
            'total_qrs': total_qrs,
            'active_qrs': active_qrs,
            'paused_qrs': paused_qrs,
        }
    )


@login_required
def active_qrs(request):
    qrs = QRCode.objects.filter(user=request.user, is_active=True).order_by('-created_at')
    return render(request, 'qrapp/my_qrs.html', {
        'qrs': qrs,
        'active_filter': 'active',
        'total_qrs': QRCode.objects.filter(user=request.user).count(),
        'active_qrs': qrs.count(),
        'paused_qrs': QRCode.objects.filter(user=request.user, is_active=False).count(),
    })


@login_required
def paused_qrs(request):
    qrs = QRCode.objects.filter(user=request.user, is_active=False).order_by('-created_at')
    return render(request, 'qrapp/my_qrs.html', {
        'qrs': qrs,
        'active_filter': 'paused',
        'total_qrs': QRCode.objects.filter(user=request.user).count(),
        'active_qrs': QRCode.objects.filter(user=request.user, is_active=True).count(),
        'paused_qrs': qrs.count(),
    })


@login_required
def edit_qr(request, id):
    qr = get_object_or_404(QRCode, id=id, user=request.user)

    if request.method == 'POST':
        new_url = request.POST.get('url')
        new_short_code = request.POST.get('short_code', '').strip()

        # Validate short_code uniqueness
        if new_short_code and QRCode.objects.filter(short_code=new_short_code).exclude(id=qr.id).exists():
            return render(request, 'qrapp/edit_qr.html', {
                'qr': qr,
                'error': 'This short code is already taken. Try another.'
            })

        if new_url != '__keep__':
            qr.url = new_url
        if new_short_code:
            qr.short_code = new_short_code

        # Regenerate QR only if URL changed
        if new_url != '__keep__':
            track_url = f'http://127.0.0.1:8000/scan/{qr.id}/'
            img = qrcode.make(track_url)
            buffer = BytesIO()
            img.save(buffer)
            qr.qr_image.save(qr.qr_image.name, File(buffer), save=False)

        qr.save()
        return redirect('my_qrs')

    return render(request, 'qrapp/edit_qr.html', {'qr': qr})


@login_required
def delete_qr(request, id):

    qr = get_object_or_404(
        QRCode,
        id=id,
        user=request.user
    )

    qr.delete()

    return redirect('my_qrs')


@login_required
def toggle_qr(request, id):

    qr = get_object_or_404(
        QRCode,
        id=id,
        user=request.user
    )

    qr.is_active = not qr.is_active
    qr.save()

    return redirect('my_qrs')

def scan_qr(request, id):
    qr = get_object_or_404(QRCode, id=id)
    qr.scans += 1
    qr.save()
    return HttpResponseRedirect(qr.url)


def short_redirect(request, short_code):
    qr = get_object_or_404(QRCode, short_code=short_code)
    qr.scans += 1
    qr.save()
    return HttpResponseRedirect(qr.url)
