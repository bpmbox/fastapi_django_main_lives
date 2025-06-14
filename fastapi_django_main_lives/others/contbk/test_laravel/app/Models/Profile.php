namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Profile extends Model
{
    protected $fillable = [
        'user_id',
        'bio',
        'tags',
    ]

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}