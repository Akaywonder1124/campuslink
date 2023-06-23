TORTOISE_ORM = {
    "connections": {"default": "sqlite://myevent.sqlite3"},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}




































































# arr = [1,1,2,2,3, 3,3]
# arr_set = set(arr)
# for i in arr_set:
#     s = arr.count(i)
#     if s == i and i == max(arr):
#         print(i)
#     else:
#         print(-1)