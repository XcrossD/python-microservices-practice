import pika, json, os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

from products.models import Product

params = pika.URLParameters('amqps://fpirdcnu:f7tQVuLEYK7MlJNkYJJn_cDoegId2e_q@shrimp.rmq.cloudamqp.com/fpirdcnu')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, methods, properties, body):
    print('Received in admin')
    data = json.loads(body)
    print(data)
    product = Product.objects.get(id=data)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

channel.close()