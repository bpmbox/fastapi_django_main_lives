<?php

namespace App\Providers;

use Illuminate\Support\Facades\URL;
use Illuminate\Support\Facades\Vite;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        // Viteのプリフェッチ設定
        Vite::prefetch(concurrency: 3);

        // 環境がlocal以外なら強制的にHTTPSを使うURLを生成する
        if (config('app.env') !== 'local') {
            URL::forceScheme('https');
        }
    }
}
