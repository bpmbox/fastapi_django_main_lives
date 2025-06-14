<?php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\ShopFrontDetails;
use App\Models\User;
use App\Models\UserProfile;

class ShopFrontController extends Controller
{
    public function index(Request $request)
    {
        $shop_front_details = ShopFrontDetails::find($request->customer_id);
        $is_required_privacy_info = $shop_front_details->is_required_privacy_info;
        $privacy_info_validation = $shop_front_details->privacy_info_validation;

        $is_privacy_info_validation = [
            'name' => false,
            'address' => false,
        ];

        if ($is_required_privacy_info == 1) {
            $privacy_info_validation_array = explode(',', $privacy_info_validation);
            if (in_array('name', $privacy_info_validation_array)) {
                $is_privacy_info_validation['name'] = true;
            }
            if (in_array('address', $privacy_info_validation_array)) {
                $is_privacy_info_validation['address'] = true;
            }
        }

        $user_profile = '';
        $user = User::where('customer_id', $shop_front_details->customer_id)->first();
        if ($user !== null) {
            $userProfile = UserProfile::where('user_id', $user->id)->first();
            if ($userProfile !== null) {
                $user_profile = json_encode($userProfile->toArray());
            }
        }

        $seiyaku_price = $this->getSeiyakuPrice($shop_front_details);

        $array = [
            "is_required_privacy_info" => $is_required_privacy_info,
            "is_privacy_info_validation" => json_encode($is_privacy_info_validation),
            "shop_front_details" => $shop_front_details,
            "tel" => $shop_front_details->tel,
            "gender" => $shop_front_details->gender,
            "email" => $shop_front_details->email,
            "user_profile" => $user_profile,
            "seiyaku_price" => $seiyaku_price,
        ];

        return view("shop_front.shop_front", $array);
    }

    private function getSeiyakuPrice(ShopFrontDetails $shop_front_details)
    {
        // implement logic to get seiyaku price
        return 0; // placeholder
    }
}