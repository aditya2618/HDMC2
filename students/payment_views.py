import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Admission
from .forms import AdmissionForm
from django.core.mail import send_mail

# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def admission_form(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST, request.FILES)
        if form.is_valid():
            admission = form.save(commit=False)
            # Create Razorpay order
            amount = 50000  # e.g. Rs 500.00 (in paise)
            order = razorpay_client.order.create({
                'amount': amount,
                'currency': 'INR',
                'payment_capture': '1'
            })
            admission.razorpay_order_id = order['id']
            admission.save()
            # Pass order info to template for Razorpay Checkout
            return render(request, 'payment.html', {
                'order_id': order['id'],
                'amount': amount,
                'admission_id': admission.id,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'name': admission.name,
                'aadhaar_no': admission.aadhaar_no,
                'email': admission.email,
                'admission_class': admission.admission_class
            })
    else:
        form = AdmissionForm()
    return render(request, 'admission_form.html', {'form': form})

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')
        admission_id = request.POST.get('admission_id')
        admission = Admission.objects.get(id=admission_id)
        # Verify payment signature
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            admission.payment_status = 'Paid'
            admission.razorpay_payment_id = payment_id
            admission.razorpay_signature = signature
            admission.save()
            # Send confirmation email
            send_mail(
                'Admission Payment Successful',
                'Your payment was successful. Admission is confirmed.',
                settings.DEFAULT_FROM_EMAIL,
                [admission.email],
                fail_silently=True
            )
            return render(request, 'receipt.html', {'admission': admission})
        except Exception:
            admission.payment_status = 'Failed'
            admission.save()
            return render(request, 'payment_failed.html')
    return redirect('admission_form')
