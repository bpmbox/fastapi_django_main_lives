Route::get('/register', 'Auth\RegisterController@create')->name('register');
Route::post('/register', 'Auth\RegisterController@store')->name('register.store');

Route::get('/login', 'Auth\LoginController@create')->name('login');
Route::post('/login', 'Auth\LoginController@store')->name('login.store');

Route::get('/profiles/{user}', 'ProfileController@show')->name('users.show');
Route::get('/profiles/{user}/edit', 'ProfileController@edit')->name('users.edit');
Route::patch('/profiles/{user}', 'ProfileController@update')->name('users.update');

Route::get('/teams', 'TeamController@index')->name('teams.index');
Route::get('/teams/create', 'TeamController@create')->name('teams.create');
Route::post('/teams', 'TeamController@store')->name('teams.store');

Route::get('/users', 'UserController@index')->name('users.index');
Route::get('/users/{user}', 'UserController@show')->name('users.show');