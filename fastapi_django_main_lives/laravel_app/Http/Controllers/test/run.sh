php -d memory_limit=-1 composer install
php artisan key:generate
php artisan migrate
php artisan serve
