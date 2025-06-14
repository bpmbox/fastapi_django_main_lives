<?php

namespace App\Http\Middleware;

use Fideloper\Proxy\TrustProxies as Middleware;
use Illuminate\Http\Request;

class TrustProxies extends Middleware
{
    /**
     * ここで信頼するプロキシを指定
     * * で全てのプロキシを信頼（環境に応じてIPを指定してもOK）
     *
     * @var array|string|null
     */
    protected $proxies = '*';

    /**
     * ヘッダー設定（X-Forwarded-* ヘッダーを信頼）
     *
     * @var int
     */
    protected $headers = Request::HEADER_X_FORWARDED_ALL;
}
