from mysite.models.ride import Ride
from mysite.db.connection import connect_to_db

def create_ride(ride: Ride):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO rides (rideable_type, start_station_id, start_station_name, end_station_id, end_station_name, started_at, ended_at, member_casual) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING ride_id",
               (ride.rideable_type, ride.start_station_id, ride.start_station_name, ride.end_station_id, ride.end_station_name, ride.started_at, ride.ended_at, ride.member_casual))
    ride_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return ride_id

def read_rides():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rides")
    rides = cur.fetchall()
    conn.close()
    return rides

def read_ride(ride_id: int):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rides WHERE ride_id = %s", (ride_id,))
    ride = cur.fetchone()
    conn.close()
    return ride

def update_ride(ride: Ride):
    conn = connect_to_db()
    cur = conn.cursor()
    from mysite.interpreter.process import no_process_file
    no_process_file(ride.start_station_name, ride.end_station_name)
    cur.execute("UPDATE rides SET rideable_type = %s, start_station_id = %s, start_station_name = %s, end_station_id = %s, end_station_name = %s, started_at = %s, ended_at = %s, member_casual = %s WHERE ride_id = %s",
               (ride.rideable_type, ride.start_station_id, ride.start_station_name, ride.end_station_id, ride.end_station_name, ride.started_at, ride.ended_at, ride.member_casual, ride.ride_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_ride(ride_id: int):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM rides WHERE ride_id = %s", (ride_id,))
    conn.commit()
    cur.close()
    conn.close()