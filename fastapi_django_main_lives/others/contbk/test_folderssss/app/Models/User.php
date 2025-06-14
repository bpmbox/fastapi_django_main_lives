namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Hash;

class User extends Model
{
    protected $fillable = ['username', 'password', 'profile', 'team_id', 'tags'];

    protected $hidden = ['password'];

    public function team()
    {
        return $this->belongsTo(Team::class);
    }
}