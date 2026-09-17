from django.db import migrations


# Preserve saved avatar choices after upstream renamed the static files.
AVATAR_PATHS = {
    'profile_pictures/Firefly Create a social media avatar 6468.jpg': 'profile_pictures/girl1.jpg',
    'profile_pictures/Firefly Create a social media avatar of a asian teenage boy in casual clothing 80817.jpg': 'profile_pictures/boy1.jpg',
    'profile_pictures/Firefly Create a social media avatar of a boy 13859.jpg': 'profile_pictures/boy2.jpg',
    'profile_pictures/Firefly Create a social media avatar of a city 87782.jpg': 'profile_pictures/city.jpg',
    'profile_pictures/Firefly Create a social media avatar of a cute beetle 25874.jpg': 'profile_pictures/beetle.jpg',
    'profile_pictures/Firefly Create a social media avatar of a cute clownfish 62786.jpg': 'profile_pictures/clownfish.jpg',
    'profile_pictures/Firefly Create a social media avatar of a cute piranha 47444.jpg': 'profile_pictures/piranha.jpg',
    'profile_pictures/Firefly Create a social media avatar of a cute red panda 35644.jpg': 'profile_pictures/red-panda.jpg',
    'profile_pictures/Firefly Create a social media avatar of a ginger person 20476.jpg': 'profile_pictures/woman1.jpg',
    'profile_pictures/Firefly Create a social media avatar of a highland cow 26215.jpg': 'profile_pictures/cow.jpg',
    'profile_pictures/Firefly Create a social media avatar of a man 33298.jpg': 'profile_pictures/man1.jpg',
    'profile_pictures/Firefly Create a social media avatar of a man 41848.jpg': 'profile_pictures/man2.jpg',
    'profile_pictures/Firefly Create a social media avatar of a mouse 40044.jpg': 'profile_pictures/mouse.jpg',
    'profile_pictures/Firefly Create a social media avatar of a non-binary person 83699.jpg': 'profile_pictures/woman2.jpg',
    'profile_pictures/Firefly Create a social media avatar of a panda 53933.jpg': 'profile_pictures/panda.jpg',
    'profile_pictures/Firefly Create a social media avatar of a rabbit 47608.jpg': 'profile_pictures/rabbit.jpg',
    'profile_pictures/Firefly Create a social media avatar of a south asian woman in casual clothing 68094.jpg': 'profile_pictures/woman3.jpg',
    'profile_pictures/Firefly Create a social media avatar of a teenage boy 39685.jpg': 'profile_pictures/boy3.jpg',
    'profile_pictures/Firefly Create a social media avatar of a teenage boy 83376.jpg': 'profile_pictures/boy4.jpg',
    'profile_pictures/Firefly Create a social media avatar of a white teenage boy 17783.jpg': 'profile_pictures/boy5.jpg',
    'profile_pictures/Firefly Create a social media avatar of an african teenage boy in casual clothing 47642.jpg': 'profile_pictures/boy6.jpg',
    'profile_pictures/Firefly Create a social media avatar of an african teenage girl in casual clothing 37307.jpg': 'profile_pictures/girl2.jpg',
    'profile_pictures/Firefly Create a social media avatar of an african teenage girl in casual clothing 96133.jpg': 'profile_pictures/girl3.jpg',
    'profile_pictures/Firefly Create a social media avatar of an african woman casual clothing 36058.jpg': 'profile_pictures/woman4.jpg',
    'profile_pictures/Firefly Create a social media avatar of an older brown woman 93089.jpg': 'profile_pictures/woman5.jpg',
    'profile_pictures/Firefly Create a social media avatar of an older man 36013.jpg': 'profile_pictures/man5.jpg',
    'profile_pictures/Firefly Create a social media avatar of an older man 6407.jpg': 'profile_pictures/man4.jpg',
    'profile_pictures/Firefly Create a social media avatar of an older person 77908.jpg': 'profile_pictures/woman6.jpg',
    'profile_pictures/Firefly Create a social media avatar of the night sky 96511.jpg': 'profile_pictures/sky.jpg',
    'profile_pictures/Firefly Create an avatar for a social media profile picture 14312.jpg': 'profile_pictures/girl5.jpg',
    'profile_pictures/Firefly Create social media avatar 15605.jpg': 'profile_pictures/person.jpg',
    'profile_pictures/Firefly Create social media avatar 433.jpg': 'profile_pictures/woman8.jpg',
    'profile_pictures/Firefly Create social media avatar of a bird 71923.jpg': 'profile_pictures/bird.jpg',
    'profile_pictures/Firefly Create social media avatar of a black cat with green eyes 36997.jpg': 'profile_pictures/cat.jpg',
    'profile_pictures/Firefly Create social media avatar of a girl 16698.jpg': 'profile_pictures/girl6.jpg',
    'profile_pictures/Firefly Create social media avatar of a golden retriever 90203.jpg': 'profile_pictures/dog.jpg',
    'profile_pictures/Firefly Create social media avatar of a penguin 54971.jpg': 'profile_pictures/penguin.jpg',
    'profile_pictures/Firefly Create social media avatar of flowers 18227.jpg': 'profile_pictures/flowers.jpg',
    'profile_pictures/Firefly Create social media profile picture of nature 14730.jpg': 'profile_pictures/nature.jpg',
    'profile_pictures/Firefly create a social media avatar for a cute dragon 88188.jpg': 'profile_pictures/dragon.jpg',
    'profile_pictures/Firefly create a social media avatar for a cute snake 58963.jpg': 'profile_pictures/snake.jpg',
    'profile_pictures/Firefly create a social media avatar of a cute axolotl 88238.jpg': 'profile_pictures/axolotl.jpg',
    'profile_pictures/Firefly create a social media avatar of a cute blobfish 46351.jpg': 'profile_pictures/pufferfish.jpg',
    'profile_pictures/Firefly create a social media avatar of a cute pigeon 6732.jpg': 'profile_pictures/pigeon.jpg',
    'profile_pictures/Firefly create a social media avatar of a white ginger man 4418.jpg': 'profile_pictures/man3.jpg',
    'profile_pictures/Firefly create a social media avatar of an east asian teenage girl 71781.jpg': 'profile_pictures/girl4.jpg',
    'profile_pictures/Firefly create a social media avatar of shrek 27880.jpg': 'profile_pictures/woman7.jpg',
    'profile_pictures/Firefly social media avatar of a cute tiger 81472.jpg': 'profile_pictures/tiger.jpg',
}


def rename_avatars(apps, schema_editor):
    profiles = apps.get_model('peer_support', 'UserProfile').objects.using(schema_editor.connection.alias)
    for old_path, new_path in AVATAR_PATHS.items():
        profiles.filter(profile_picture=old_path).update(profile_picture=new_path)


def restore_avatars(apps, schema_editor):
    profiles = apps.get_model('peer_support', 'UserProfile').objects.using(schema_editor.connection.alias)
    for old_path, new_path in AVATAR_PATHS.items():
        profiles.filter(profile_picture=new_path).update(profile_picture=old_path)


class Migration(migrations.Migration):
    dependencies = [('peer_support', '0002_upstream_model_updates')]
    operations = [migrations.RunPython(rename_avatars, restore_avatars)]
