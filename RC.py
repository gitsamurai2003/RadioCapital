import flet as ft

#define a song class as our model 
class Song(object):
    def __init__(self, song_name: str, artist_name: str,
    audio_path: str, img_path: str) -> None:
        super(Song, self).__init__()
        self.song_name: str = song_name
        self.artist_name: str = artist_name
        self.audio_path: str = audio_path
        self.img_path: str = img_path
    
    #define a properties for this class to access each attribute 
    @property
    def name(self) -> str:
        return self.song_name

    @property
    def artist(self) -> str:
        return self.artist_name
    
    @property
    def audio(self) -> str:
        return self.audio_path

    @property
    def img(self) -> str:
        return self.img_path
    

#next, define a directory class where we store individual songs
class AudioDirectory(object):
    playlist: list = [
        Song(
            song_name="Windmill Isle - Day",
            artist_name="Tomoya Ohtani",
            audio_path="Windmill Isle - Day    SONIC UNLEASHED.mp3",
            img_path="1200x1200bb.jpg",
        ),
        Song(
            song_name="Requiem",
            artist_name="W. A. Mozart",
            audio_path="Wolfgang_Amadeus_Mozart_Requiem.mp3",
            img_path="wolfgang-amadeus-mozart-cloaks-hat-cityscape-wallpaper-thumb.jpg",
        ),
    ]


#our first page/view is the playlist
class Playlist(ft.View):
    def __init__(self, page: ft.Page) -> None:
        super(Playlist, self).__init__(
            route="/playlist",
            horizontal_alignment="center"
        )
         
        self.page = page
        self.playlist: list[Song] = AudioDirectory.playlist

        self.controls = [
            ft.Row(
                [
                    ft.Text("PLAYLIST", size = 21, weight="bold"),
                ],
                alignment="center"
            ),
            ft.Divider(height=10, color="transparent")
        ]


        self.generate_playlist_ui()


    #define a method to add the songs from the playlist
    def generate_playlist_ui(self) -> None:
        for song in self.playlist:
            self.controls.append(
                self.create_song_row(
                    #you can also use the properties defined in the Song class here ...
                    song_name=song.song_name,
                    artist_name=song.artist_name,
                    song=song
                )
            )

    def create_song_row(self, song_name, artist_name, song: Song):
            return ft.Container(
                content=ft.Row(
                    [
                        ft.Text(f"Title: {song.name}"),
                        ft.Text(artist_name),
                    ],
                    alignment="spaceBetween"
                ),
                data=song, #song = the song model; i.e. Song class
                padding = 10,
                on_click = self.toggle_song,
            )
        
def toggle_song(self, e) -> None:
    #to pass data between views, we store them in the 
    #page sessions
    #recall that the data of the control is the Song model
    #with all the song details and audio path
    self.page.session.set("song", e.control.data)
    self.page.go("/song")    


#before setting up the button that shows the current song, lets define a current
#song class

class CurrentSong(ft.View):
    def __init__(self, page: ft.Page) -> None:
        super(CurrentSong, self).__init__(
            route="/song",
            padding=20,
            horizontal_alignment="center",
            vertical_alignment="center",         
        )

        self.page = page
        #we can access the session data like this...
        self.song = self.page.session.get("song")


        print(self.song)



def main(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.LIGHT

    def router(route) -> None:
        page.views.clear()

        if page.route == "/playlist":
            playlist = Playlist(page)
            page.views.append(playlist)


        if page.route == "/song":
            song = CurrentSong(page)
            page.views.append(song)


        page.update()
        
    page.on_route_change = router
    page.go("/playlist")

ft.app(target=main, assets_dir="assets")