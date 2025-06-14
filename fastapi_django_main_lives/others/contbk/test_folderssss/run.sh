#!/bin/bash

# Install dependencies
composer install

# Run migrations
php artisan migrate

# Run seeds
php artisan db:seed

# Start the development server
php artisan serve
