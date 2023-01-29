import gameobjects
import images 
import sounds
import pygame

#--Contains collisions handlers wrapped in functions for creating them

def play_explosion_anim(bullet, game_objects_list, space):
    """ Playes the explosion animation at the coordinates of the bullet"""
    game_objects_list.append(bullet.explosion(space))
    
    for obj in game_objects_list.copy():
        if isinstance(obj, gameobjects.Explosion):
            if obj.stop:
                game_objects_list.remove(obj)


def remove_object(object, space, game_objects_list):
    """Removes object from sapce and game object list"""
    space.remove(object, object.body)
    game_objects_list.remove(object.parent)


def create_ind_box_handler(game_objects_list, space):
    """Returns a collision handler for bullets and
    indestructable boxes"""
    def ind_collision_bullet_box(arb, space, data):
        """Handels collisions between bullets and indestructable objects"""
        bullet_shape = arb.shapes[0]
        if bullet_shape.parent in game_objects_list:
            remove_object(bullet_shape, space, game_objects_list)
            play_explosion_anim(bullet_shape.parent, game_objects_list, space)
        return False
    
    return ind_collision_bullet_box


def create_bullet_box_handler(game_objects_list, space):
    """Returns a collision handler for bullets and
    boxes"""
    def collision_bullet_box(arb, space, data):
        """Handles collisions between bullets and boxes"""
        bullet_shape = arb.shapes[0]
        box = arb.shapes[1]
        sounds.box_sound.set_volume(0.2)
        sounds.box_sound.play()
        if bullet_shape.parent in game_objects_list:
            remove_object(bullet_shape, space, game_objects_list)
            
            remove_object(box, space, game_objects_list)

            play_explosion_anim(bullet_shape.parent,
             game_objects_list, space)
        return False
    
    return collision_bullet_box


def create_bullet_tank_handler(game_objects_list, space, flag):
    """Returns a collision handler for bullets and
    tanks"""
    def collision_bullet_tank(arb, space, data):
        """Handles collisions between tanks and bullets"""
        bullet_shape = arb.shapes[0]
        tank = arb.shapes[1].parent

        if tank != bullet_shape.parent.tank:
            if bullet_shape.parent in game_objects_list:
                remove_object(bullet_shape, space, game_objects_list)
                play_explosion_anim(bullet_shape.parent,
                 game_objects_list, space)
                # If 2000 ticks have passed since tak respawn
                # check tank hit points
                if pygame.time.get_ticks() - tank.get_respawn_time() > 2500:
                    # Remove 1 hp from the tank
                    tank.decrease_hp()
                    # If the tank has 0 hp respawn it
                    if tank.get_hit_points() == 0:
                        # Save time of death
                        tank.set_respawn_time(pygame.time.get_ticks())
                        sounds.tank_shot_sound.play()
                        tank.respawn()
                        tank.drop_flag(flag)

        return False

    return collision_bullet_tank


def create_bullet_bullet_handler(game_objects_list, space):
    """Returns a collision handler for bullets and bullets"""
    def collision_bullet_bullet(arb, space, data):
        """Handles collisions between tanks and bullets"""
        bullet1 = arb.shapes[0]
        bullet2 = arb.shapes[1]
        if bullet2.parent in game_objects_list:
            space.remove(bullet1, bullet1.body)
            game_objects_list.remove(bullet1.parent)

        if bullet2.parent in game_objects_list:
            space.remove(bullet2, bullet2.body)
            game_objects_list.remove(bullet2.parent)
        play_explosion_anim(bullet1.parent, game_objects_list, space)
        return False

    return collision_bullet_bullet