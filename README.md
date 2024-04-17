/api/gifts category price_range sort_by limit. Метод Get.

пример запроса: /api/gifts?category=birthday&?price_range=200-300&?limit=2&sort_by=name\price

пример ответа:
 
     1,   
    "Flower Bouquet",
    "Beautiful bouquet of flowers",
    "birthday",
    25.99
    
  
  
    2,
    "Chocolate Box",
    "Delicious assorted chocolates",
    "valentine",
    15.49
  
/api/gift/<int:gift_id> Метод Get.

пример ответа:

  1,
  "Flower Bouquet",
  "Beautiful bouquet of flowers",
  "birthday",
  25.99

ответ включает следующие поля: id, name, description, category, price

/api/register - методом POST!

Принимает следующие поля:

username, password, name, email.

