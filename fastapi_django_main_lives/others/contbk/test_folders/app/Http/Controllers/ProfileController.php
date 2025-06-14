<?php
namespace App\Http\Controllers;

use App\Models\Profile;
use Illuminate\Http\Request;

class ProfileController extends Controller
{
    public function edit(User $user)
    {
        $profile = $user->profile;

        return view('profiles.edit', compact('profile'));
    }

    public function update(Request $request, User $user)
    {
        $request->validate([
            'bio' => 'required|string|max:255',
            'tags' => 'required|array',
        ]);

        $profile = $user->profile;

        $profile->bio = $request->input('bio');
        $profile->tags = $request->input('tags');

        $profile->save();

        return redirect()->route('users.show', $user);
    }
}