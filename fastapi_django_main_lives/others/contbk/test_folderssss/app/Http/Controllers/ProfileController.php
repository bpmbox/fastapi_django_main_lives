namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;

class ProfileController extends Controller
{
    public function update(Request $request, $id)
    {
        $user = User::find($id);
        if (!$user) {
            return response()->json(['message' => 'User not found'], 404);
        }

        $request->validate([
            'profile' => 'required',
            'team_id' => 'required',
            'tags' => 'required',
        ]);

        $user->profile = $request->profile;
        $user->team_id = $request->team_id;
        $user->tags = $request->tags;
        $user->save();

        return response()->json(['message' => 'Profile updated successfully'], 200);
    }
}