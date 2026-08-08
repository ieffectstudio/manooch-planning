page https://admin.manooch.site/payment-link


curl --url ^"https://api.manooch.site/admin/stores/5fbc7ad7-8abb-4aa7-843c-565a51a1241e/payment-links^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlZmQzOTExYS04M2Y1LTQxNzQtOWRjYi0zOWYxZDdiZGI2ZmYiLCJtb2JpbGUiOiIwOTkyODQ1NjI4NSIsImp0aSI6IjgyNWU3ZDk3LTA3ODQtNDRhNy1iZTczLWE5ODEzYTQwMTNlOCIsImlhdCI6MTc4NjAxODMxMCwiZXhwIjoxNzg4NjEwMzEwfQ.kWHpvT-oVPRxhihaz2V-WY_QDIBprE33x8LrXKFQXJo^" ^
  -H ^"Referer: https://admin.manooch.site/^" ^
  -H ^"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36^" ^
  -H ^"sec-ch-ua: ^\^"Not=A?Brand^\^";v=^\^"99^\^", ^\^"Google Chrome^\^";v=^\^"151^\^", ^\^"Chromium^\^";v=^\^"151^\^"^" ^
  -H ^"Content-Type: application/json^" ^
  -H ^"sec-ch-ua-mobile: ?0^"

 
  {
    "statusCode": 500,
    "success": false,
    "message": "خطای داخلی سرور رخ داده است",
    "data": null,
    "errors": [
        {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "خطای داخلی سرور رخ داده است"
        }
    ]
}



give me plan for fix this bug & here is server ssh :  
ssh manooch-server