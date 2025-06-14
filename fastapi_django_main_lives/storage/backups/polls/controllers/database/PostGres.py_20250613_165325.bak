import gradio as gr
import psycopg2
from dataclasses import dataclass, field
from typing import List, Optional
from mysite.interpreter.process import no_process_file,process_file

@dataclass
class Ride:
    ride_id: Optional[int] = field(default=None)
    rideable_type: str = ''
    start_station_id: int = 0
    start_station_name: str = ''
    end_station_id: int = 0
    end_station_name: str = ''
    started_at: str = ''
    ended_at: str = ''
    member_casual: str = ''

def connect_to_db():
    conn = psycopg2.connect(
        dbname="neondb",
        user=os.getenv("postgre_user"),
        password=os.getenv("postgre_pass"),
        host=os.getenv("postgre_host"),
        port=5432,
        sslmode="require"
    )
    return conn

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
    no_process_file(ride.start_station_name,ride.end_station_name)
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

#def crud_interface():
with gr.Blocks() as gradio_interface:
    with gr.Row():
        rideable_type = gr.Textbox(label="Rideable Type")
        start_station_id = gr.Number(label="Start Station ID")
        start_station_name = gr.Textbox(label="Start Station Name")
        end_station_id = gr.Number(label="End Station ID")
        end_station_name = gr.Textbox(label="End Station Name")
        started_at = gr.Textbox(label="Started At")
        ended_at = gr.Textbox(label="Ended At")
        member_casual = gr.Textbox(label="Member Casual")
        ride_id = gr.Number(label="Ride ID (for update/delete)", value=-1, interactive=False)

    create_button = gr.Button("Create Ride")
    update_button = gr.Button("Update Ride")
    delete_button = gr.Button("Delete Ride")
    read_button = gr.Button("Read Rides")
    output = gr.Dataframe(headers=["Ride ID", "Rideable Type", "Start Station ID", "Start Station Name", "End Station ID", "End Station Name", "Started At", "Ended At", "Member Casual"])

    def create_ride_click(rideable_type, start_station_id, start_station_name, end_station_id, end_station_name, started_at, ended_at, member_casual):
        ride = Ride(
            rideable_type=rideable_type,
            start_station_id=start_station_id,
            start_station_name=start_station_name,
            end_station_id=end_station_id,
            end_station_name=end_station_name,
            started_at=started_at,
            ended_at=ended_at,
            member_casual=member_casual
        )
        create_ride(ride)
        return [[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]] for r in read_rides()]

    def update_ride_click(ride_id, rideable_type, start_station_id, start_station_name, end_station_id, end_station_name, started_at, ended_at, member_casual):
        ride = Ride(
            ride_id=int(ride_id),
            rideable_type=rideable_type,
            start_station_id=start_station_id,
            start_station_name=start_station_name,
            end_station_id=end_station_id,
            end_station_name=end_station_name,
            started_at=started_at,
            ended_at=ended_at,
            member_casual=member_casual
        )
        update_ride(ride)
        return [[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]] for r in read_rides()]

    def delete_ride_click(ride_id):
        delete_ride(int(ride_id))
        return [[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]] for r in read_rides()]

    def read_rides_click():
        return [[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]] for r in read_rides()]

    def load_ride_details(evt: gr.SelectData):
        row_index = evt.index[0] if isinstance(evt.index, list) else evt.index
        rides = read_rides()
        selected_row = rides[row_index]
        ride_id = selected_row[0]
        ride = read_ride(ride_id)
        if ride:
            return ride[1], ride[2], ride[3], ride[4], ride[5], ride[6], ride[7], ride[8], ride[0]
        return "", 0, "", 0, "", "", "", "", -1

    create_button.click(fn=create_ride_click, 
                        inputs=[rideable_type, start_station_id, start_station_name, end_station_id, end_station_name, started_at, ended_at, member_casual], 
                        outputs=output)
    update_button.click(fn=update_ride_click, 
                        inputs=[ride_id, rideable_type, start_station_id, start_station_name, end_station_id, end_station_name, started_at, ended_at, member_casual], 
                        outputs=output)
    delete_button.click(fn=delete_ride_click, inputs=ride_id, outputs=output)
    read_button.click(fn=read_rides_click, outputs=output)
    
    output.select(fn=load_ride_details, inputs=None, outputs=[rideable_type, start_station_id, start_station_name, end_station_id, end_station_name, started_at, ended_at, member_casual, ride_id])

#return interface

#d1 = crud_interface()
#d1.launch()
