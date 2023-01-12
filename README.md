# Simple RESTful API for a social networking application

FastAPI project for a social network with users, posts, like/dislike system. 

<img src="https://sun9-88.userapi.com/impg/mIqZ3uI-H_fyxKg29rUeqW7gVmNCUrGNVRjAsQ/55FeeSzPPiE.jpg?size=1430x938&quality=96&sign=286e92333a8a17e95195a95a21cc36af&type=album" alt="drawing" width="720" height="469"/>

# How to use it
1. Clone repository.
2. Navigate to the project folder and run `docker-compose up --build` in your terminal.
3. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to see API Swagger docs.
4. Open [http://127.0.0.1:5050](http://127.0.0.1:5050) to login into PGAdmin.
5. To login into your user account in API press Authorize button and enter your `Email` and `Password`.

# PGAdmin
![PGAdmin](https://sun9-85.userapi.com/impg/Ypo0eOUAXkJi7_pyB-dbXBBeckAphgFq6T_v0Q/hVhT3gckMyI.jpg?size=471x293&quality=96&sign=9a8db6cd93356c6361e61413f3d97421&type=album)

- To login into PGAdmin use these credentials:
- - Email: `admin@example.com`
- - Password: `password`

Then register new server:

![Service](https://sun9-80.userapi.com/impg/AbJd5EMfyLToWxb9_h59c2ZufQcvMxVsSg-W8w/aJVUlsaXyug.jpg?size=517x221&quality=96&sign=15063dda972543ebe9935f88f5d2b917&type=album)

- Fill next fields with credentials:
- - General -> Name - `db`
- - Connection -> Host Name - `db`
- - Connection -> Username - `postgres`
- - Connection -> Password - `password`
