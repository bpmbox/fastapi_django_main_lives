namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class ProfileRequest extends FormRequest
{
    public function rules()
    {
        return [
            'bio' => 'required|string',
            'tags' => 'required|string',
        ];
    }
}