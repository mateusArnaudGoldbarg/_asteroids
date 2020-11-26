"""
File: asteroids.py
Original Author: Mateus Arnaud Goldbarg
Date: 06/03/2020
This program implements the asteroids game.
"""

import arcade
import random
import math
from point import Point
from velocity import Velocity
from abc import ABC,abstractmethod

large = "images/meteorGrey_big1.png"
medium = "images/meteorGrey_med1.png"
small = "images/meteorGrey_small1.png"
laser = "images/laserBlue01.png"
ship = "images/playerShip1_orange.png"
"""
Creativity: 
1 - Noise for bullets
2 - noise for explosions
3 - You Won text after winning the game
4 - Game Over after loosing the game
5 - score counter
6 - number of asteroids counter
7 - Asteroids beggining at the edges of the screen (not just in bottom left (0,0)
"""
# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

class Flying_objects(ABC):
    """
    class for every object that corss the screen
    """
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        self.angle = 0
        self.radius = 0

    def advance(self):
        """
        Default method for advance flying objects
        :return:
        """
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        self.is_off_screen(SCREEN_WIDTH,SCREEN_HEIGHT)

    def is_off_screen(self, WIDTH, HEIGHT):
        """
        Test if the obj is of screen
        :param WIDTH:
        :param HEIGHT:
        :return:
        """
        if self.center.x >= WIDTH + 50:
            self.center.x = -50

        elif self.center.x <= -50:
            self.center.x = WIDTH + 50

        if self.center.y >= HEIGHT + 50:
            self.center.y = -50

        elif self.center.y <= -50:
            self.center.y = HEIGHT + 50

    @abstractmethod
    def draw(self):
        pass

class Asteroids(Flying_objects,ABC):
    """
    Abstract class for every asteroids
    """
    def __init__(self):
        super().__init__()
        '''
        hit_type = 1 - killed the Large Asteroid
        hit_type = 2 - Killed the Medium Asteroid
        '''
        #self.angle = 0
        self.son_asteroids = []

    @abstractmethod
    def hits(self):
        """
        Abstract method to check the hits
        :return:
        """
        pass

class Large_Asteroid(Asteroids):
    """
    Large asteroids class
    """
    def __init__(self):
        super().__init__()
        self.radius = 15
        teta = random.uniform(0, 360)
        self.velocity.dx = 1.5 * math.cos(math.radians(teta)) #RANDOM VELOCITY IN X
        self.velocity.dy = 1.5 * math.sin(math.radians(teta)) #RANDOM VELOCITY IN Y
        self.position_init()


    def hits(self):
        """
        hit_type = 1: Type When hit a large asteroid, it will become
        2 medium asteroids and 1 small asteroid
        :return:
        """
        medium1 = Medium_Asteroid(self.center.x, self.center.y,0,-2)
        medium2 = Medium_Asteroid(self.center.x, self.center.y, 0, 2)
        small = Small_Asteroid(self.center.x, self.center.y, 5, 0)
        self.son_asteroids = [medium1,medium2,small]
        return self.son_asteroids


    def advance(self):
        """
        method for advance the large asteroid
        :return:
        """
        self.angle += 1
        super().advance()

    def draw(self):
        """
        Method to draw Asteroid
        :return:
        """
        texture = arcade.load_texture(large)
        alpha = 255

        width = texture.width
        height = texture.height

        arcade.draw_texture_rectangle(self.center.x, self.center.y, width, height, texture, self.angle, alpha)

    def position_init(self):
        """
        radom choise to the direction of the new asteroid
        :return:
        """
        opt = random.randint(1,4)

        if opt == 1:
            self.center.x = 0
            self.center.y = random.randint(0, SCREEN_HEIGHT)

        elif opt == 2:
            self.center.x = random.randint(0, SCREEN_WIDTH)
            self.center.y = 0

        elif opt == 3:
            self.center.x = SCREEN_WIDTH
            self.center.y = random.randint(0, SCREEN_HEIGHT)

        elif opt == 4:
            self.center.x = random.randint(0, SCREEN_WIDTH)
            self.center.y = SCREEN_HEIGHT

class Medium_Asteroid(Asteroids):
    """
    Medium asteroids class
    """
    def __init__(self,center_x,center_y,vel_x,vel_y):
        """
        Parameters are the position and velocity of the Large Asteroid
        :param center_x:
        :param center_y:
        :param vel_x:
        :param vel_y:
        """
        super().__init__()
        self.radius = 5
        self.center.x = center_x
        self.center.y = center_y
        self.velocity.dx += vel_x
        self.velocity.dy += vel_y

    def draw(self):
        """
        Draw method for Medium Asteroid
        :return:
        """
        texture = arcade.load_texture(medium)
        alpha = 255

        width = texture.width
        height = texture.height

        arcade.draw_texture_rectangle(self.center.x, self.center.y, width, height, texture, self.angle, alpha)

    def hits(self):
        """
        hit_type = 2 -> when hit one medium asteroid it will become two small asteroids
        :return:
        """
        small1 = Small_Asteroid(self.center.x, self.center.y, 1.5, 1.5)
        small2 = Small_Asteroid(self.center.x, self.center.y, -1.5, -1.5 )
        self.son_asteroids = [small1, small2]
        return self.son_asteroids

    def advance(self):
        """
        Advance method for medium asteroid
        :return:
        """
        self.angle -= 2

        super().advance()

class Small_Asteroid(Asteroids):
    """
    Small asteroids class
    """
    def __init__(self,center_x,center_y,vel_x,vel_y):
        """
        Parameters are the position and velocity of Medium Asteroid or Large Asteroid
        :param center_x:
        :param center_y:
        :param vel_x:
        :param vel_y:
        """
        super().__init__()
        self.radius = 2
        self.center.x = center_x
        self.center.y = center_y
        self.velocity.dx += vel_x
        self.velocity.dy += vel_y

    def draw(self):
        """
        Draw method for small asteroid
        :return:
        """
        texture = arcade.load_texture(small)
        alpha = 255

        width = texture.width
        height = texture.height
        arcade.draw_texture_rectangle(self.center.x, self.center.y, width, height, texture, self.angle, alpha)

    def hits(self):
        """
        Small asteroid just die when is hited
        :return:
        """
        return []

    def advance(self):
        """
        Advance method for small asteroids
        :return:
        """
        self.angle += 5
        super().advance()

class Ship(Flying_objects):
    """
    Class for ship
    """
    def __init__(self):
        super().__init__()
        #self.angle = 0
        self.center.x = SCREEN_WIDTH / 2
        self.center.y = SCREEN_HEIGHT / 2
        self.radius = 30
        #self.state = -1

    def advance_left(self):
        """
        Change the angle when press left
        :return:
        """
        self.angle += 3

    def advance_right(self):
        """
        Change the angle when press right
        :return:
        """
        self.angle -= 3

    def advance_up(self):
        """
        move the ship across the screen, is the thrust of the ship
        :return:
        """

        self.velocity.dy += 0.25 * math.sin(self.angle * math.pi / 180)
        self.velocity.dx += 0.25 * math.cos(self.angle * math.pi / 180)

        if self.velocity.dx >= 30:
            self.velocity.dx = 30

        if self.velocity.dy >= 30:
            self.velocity.dy = 30

        #self.state = 1

    def advance_down(self):
        pass

    def draw(self):
        """
        Draw method for the ship
        :return:
        """
        texture = arcade.load_texture(ship)
        alpha = 255
        width = texture.width
        height = texture.height
        arcade.draw_texture_rectangle(self.center.x, self.center.y, width, height, texture, self.angle - 90, alpha)


class Bullets(Flying_objects):
    """
    Class for bullets
    """
    def __init__(self,Ship):
        """
        Bulleet will take the velocity, angle and position of the Ship
        :param Ship:
        """
        super().__init__()
        self.angle = Ship.angle
        #self.velocity.dx = 10 * math.cos(math.radians(self.angle))
        #self.velocity.dy = 10 * math.sin(math.radians(self.angle))
        self.center.x = Ship.center.x
        self.center.y = Ship.center.y
        self.velocity.dx = Ship.velocity.dx
        self.velocity.dy = Ship.velocity.dy
        self.radius = 10
        self.frame_travel = 0 # To check if is time to kill the bullet

    def draw(self):
        """
        Draw function of the bullets
        :return:
        """
        texture = arcade.load_texture(laser)
        alpha = 255

        width = texture.width
        height = texture.height
        arcade.draw_texture_rectangle(self.center.x, self.center.y, width, height, texture, self.angle, alpha)

    def fire(self):
        """
        Get velocity the ship and add to the velocity of the bullet
        It makes the inertia workds
        :return:
        """
        self.velocity.dx += 10 * math.cos(math.radians(self.angle))
        self.velocity.dy += 10 * math.sin(math.radians(self.angle))

    def advance(self):
        super().advance()
        self.frame_travel += 1
        if self.frame_travel >=60:
            self.alive = False

class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()
        #self.last_pos_x = 0
        #self.last_pos_y = 0
        # TODO: declare anything here you need the game class to track
        self.asteroids = []
        self.bullets = []
        self.ship = Ship()
        self.state_init = 0
        '''
        state_init = 0 - Initialize the game
        state_init = 2 - Game Over
        state_init = 3 - YOU WON 
        '''
        self.music = None
        self.score = 0

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        arcade.draw_text("by Mateus Arnaud Goldbarg", start_x=0, start_y=SCREEN_HEIGHT - 30, font_size=12, color=arcade.color.WHITE)
        arcade.draw_text("SCORE: {} - ASTEROIDS: {}".format(self.score,len(self.asteroids)), start_x=0, start_y=0, font_size=12, color=arcade.color.YELLOW) #SCORE AND N°  ASTEROIDS
        # TODO: draw each object
        if self.ship.alive == True:
            self.ship.draw()

        if self.state_init == 2:
            arcade.draw_text("GAME OVER", start_x=SCREEN_WIDTH/4, start_y=SCREEN_HEIGHT/2, font_size=60, color=arcade.color.WHITE,bold=True)

        elif self.state_init == 3:
            arcade.draw_text("YOU WON!!", start_x=SCREEN_WIDTH / 4, start_y=SCREEN_HEIGHT / 2, font_size=60, color=arcade.color.WHITE, bold=True)

        for asteroid in self.asteroids:
            asteroid.draw()

        for bullet in self.bullets:
            bullet.draw()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()

        # TODO: Tell everything to advance or move forward one step in time

        self.ship.advance()

        self.check_collision()
        for asteroid in self.asteroids:
            asteroid.advance()

        for bullet in self.bullets:
            bullet.advance()

        self.create_asteroid()

        # TODO: Check for collisions
    def check_collision(self):
        """
        Check the collisions of the game
        :return:
        """
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if bullet.alive and asteroid.alive:
                    too_close = bullet.radius + asteroid.radius

                    if (abs(bullet.center.x - asteroid.center.x) < too_close and
                                abs(bullet.center.y - asteroid.center.y) < too_close):
                        #self.last_pos_x = asteroid.center.x
                        #self.last_pos_y = asteroid.center.y
                        bullet.alive = False
                        asteroid.alive = False
                        self.score += 1
                        self.setup2()
                        asteroid.hits()
        for asteroid in self.asteroids:
            if asteroid.alive and self.ship.alive:
                too_close_2 = self.ship.radius + asteroid.radius
                if abs(self.ship.center.x - asteroid.center.x) < too_close_2 and abs(self.ship.center.y - asteroid.center.y) < too_close_2:
                    self.ship.alive = False
                    self.state_init = 2
                    self.setup2()

        self.create_asteroid()
        self.clean()

    def clean(self):
        """
        kill bullets and asteroids
        :return:
        """
        for bullet in self.bullets:
            if bullet.alive == False:
                self.bullets.remove(bullet)
        for asteroid in self.asteroids:
            if asteroid.alive == False:
                self.asteroids.remove(asteroid)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.advance_left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.advance_right()

        if arcade.key.UP in self.held_keys:
            self.ship.advance_up()

        if arcade.key.DOWN in self.held_keys:
            self.ship.advance_down()


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """

        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                bullet = Bullets(self.ship)
                bullet.fire()
                self.bullets.append(bullet)
                self.setup()

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)

    def create_asteroid(self):
        """
        Creation of the asteroids
        :return:
        """
        #creation of the first 5 aasteroids
        if self.state_init == 0:
            while len (self.asteroids) < 5:
                large_asteroid = Large_Asteroid()
                self.asteroids.append(large_asteroid)
            self.state_init = 1
        #Create 2 mediums and 1 small when shooting the large one
        for asteroid in self.asteroids:
            if asteroid.alive == False:
                self.asteroids.extend(asteroid.hits())

        if len(self.asteroids) <= 0:
            self.state_init = 3

    def play_song(self,musica):
        """
        Play noises of the game

        :param musica:
        :return:
        """
        if self.music:
            self.music.stop()
        self.music = arcade.Sound(musica,streaming=True)
        self.music.play(0.1)

    def setup(self):
        """
        Noise for shooting
        :return:
        """
        self.musica = ":resources:sounds/laser2.wav"
        self.play_song(self.musica)

    def setup2(self):
        """
        noise for explosion
        :return:
        """
        self.musica2 = ":resources:sounds/explosion2.wav"
        self.play_song(self.musica2)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()