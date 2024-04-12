from engine.camera import Camera
from engine.content_types.texture import Texture
from engine.data_types.blend_mode import BlendMode
from engine.data_types.color import Color
from engine.lights.base_light import BaseLight
from engine.renderer import Renderer


class AmbientLight(BaseLight):
    """ A global light. """
    def __init__(self) -> None:
        super().__init__()
        self._texture = Texture.create_target(2, 2)
        self._reset_texture()

        Renderer.add_reset_callback(self._reset_texture)

    def __del__(self) -> None:
        Renderer.remove_reset_callback(self._reset_texture)

    def _reset_texture(self) -> None:
        self._texture = Texture.create_target(2, 2)
        self._texture.set_blend_mode(BlendMode.ADD)
        with Renderer.render_target(self._texture):
            Renderer.clear(Color.white())

    # noinspection DuplicatedCode
    def draw(self, camera: Camera) -> None:
        if self.intensity:
            with camera.render_pass("Lighting"):
                Renderer.set_texture_color_mod(self._texture, self.color)
                Renderer.set_texture_alpha_mod(self._texture, int(self._intensity * 255))

                Renderer.copy(
                    texture=self._texture,
                    source_rect=None,
                    destination_rect=None,
                    rotation_angle=0,
                    rotation_center=None,
                    flip=0
                )

                Renderer.clear_texture_color_mod(self._texture)
                Renderer.clear_texture_alpha_mod(self._texture)

        if self.glow_intensity:
            with camera.render_pass("Glow"):
                Renderer.set_texture_color_mod(self._texture, self.color)
                Renderer.set_texture_alpha_mod(self._texture, int(self._glow_intensity * 255))

                Renderer.copy(
                    texture=self._texture,
                    source_rect=None,
                    destination_rect=None,
                    rotation_angle=0,
                    rotation_center=None,
                    flip=0
                )

                Renderer.clear_texture_color_mod(self._texture)
                Renderer.clear_texture_alpha_mod(self._texture)
