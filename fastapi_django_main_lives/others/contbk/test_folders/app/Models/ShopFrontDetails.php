<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class ShopFrontDetails extends Model
{
    protected $fillable = [
        'is_required_privacy_info',
        'privacy_info_validation',
        'tel',
        'gender',
        'email',
        'customer_id',
        'is_limited',
    ];
}