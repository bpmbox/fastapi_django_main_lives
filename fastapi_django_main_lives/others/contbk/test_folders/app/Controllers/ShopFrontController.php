<?php

namespace App\Controllers;

use Illuminate\Http\Request;
use App\Models\ShopFrontDetails;
use App\Models\User;
use App\Models\UserProfile;
use App\Services\SeiyakuPriceService;

class ShopFrontController extends Controller
{
    public function index(Request $request, ShopFrontDetails $shopFrontDetails)
    {
        $isRequiredPrivacyInfo = $shopFrontDetails->is_required_privacy_info;
        $privacyInfoValidation = $shopFrontDetails->privacy_info_validation;
        $isPrivacyInfoValidation = $this->getPrivacyInfoValidation($privacyInfoValidation, $isRequiredPrivacyInfo);

        $userProfile = $this->getUserProfile($shopFrontDetails->customer_id);
        $seiyakuPrice = (new SeiyakuPriceService())->getSeiyakuPrice($shopFrontDetails);

        $array = [
            "is_required_privacy_info" => $isRequiredPrivacyInfo,
            "is_privacy_info_validation" => json_encode($isPrivacyInfoValidation),
            "shop_front_details" => $shopFrontDetails,
            "is_limited" => $shopFrontDetails->is_limited,
            "tel" => $shopFrontDetails->tel,
            "gender" => $shopFrontDetails->gender,
            "email" => $shopFrontDetails->email,
            "user_profile" => $userProfile,
            "seiyaku_price" => $seiyakuPrice,
        ];

        return view("shop_front.shop_front", $array);
    }

    private function getPrivacyInfoValidation($privacyInfoValidation, $isRequiredPrivacyInfo)
    {
        $isPrivacyInfoValidation = [
            'name' => false,
            'address' => false,
        ];

        if ($isRequiredPrivacyInfo == 1) {
            $privacyInfoValidationArray = explode(',', $privacyInfoValidation);
            if (in_array('name', $privacyInfoValidationArray)) {
                $isPrivacyInfoValidation['name'] = true;
            }
            if (in_array('address', $privacyInfoValidationArray)) {
                $isPrivacyInfoValidation['address'] = true;
            }
        }

        return $isPrivacyInfoValidation;
    }

    private function getUserProfile($customerId)
    {
        $user = User::where('customer_id', $customerId)->first();
        if ($user !== null) {
            $userProfile = UserProfile::where('user_id', $user->id)->first();
            if ($userProfile !== null) {
                return json_encode($userProfile->toArray());
            }
        }

        return '';
    }
}