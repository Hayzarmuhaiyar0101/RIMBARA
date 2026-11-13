
<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

// RIMBARA API STATUS
Route::get('/status', function () {
    return response()->json([
        'success' => true,
        'system' => 'RIMBARA',
        'description' => 'National Forest Fire Analysis System',
        'region' => 'Indonesia',
        'satellite' => 'Sentinel-2',
        'method' => 'Differenced Normalized Burn Ratio',
        'version' => '1.0.0',
        'status' => 'ONLINE'
    ]);
});

