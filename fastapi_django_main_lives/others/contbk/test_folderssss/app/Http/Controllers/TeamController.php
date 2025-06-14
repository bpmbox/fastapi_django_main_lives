namespace App\Http\Controllers;

use App\Models\Team;
use Illuminate\Http\Request;

class TeamController extends Controller
{
    public function index()
    {
        $teams = Team::orderBy('created_at', 'desc')->get();
        return response()->json($teams, 200);
    }

    public function store(Request $request)
    {
        $request->validate([
            'name' => 'required',
        ]);

        $team = new Team();
        $team->name = $request->name;
        $team->save();

        return response()->json(['message' => 'Team created successfully'], 201);
    }
}