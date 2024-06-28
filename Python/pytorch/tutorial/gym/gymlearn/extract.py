"""Tools to extract screen cap images from gym."""
import torch
import torchvision
import torchvision.transforms as T
import numpy as np
from PIL import Image


class GymExtractor:
    """Extract screen images from gym."""
    RESIZE = T.Compose([T.ToPILImage(),
                        T.Resize(40, interpolation=Image.CUBIC),
                        T.ToTensor()])

    SCREEN_WIDTH = 1200

    def __init__(self, gym_env, torch_device):
        self.env = gym_env
        self.device = torch_device


    def get_cart_location(self):
        """Get the location of the middle of the cart in screen space."""
        world_width = self.env.x_threshold * 2
        scale = self.SCREEN_WIDTH / world_width
        return int(self.env.state[0] * scale + self.SCREEN_WIDTH / 2.0)  # middle of cart


    def get_screen(self):
        """Grab the screen around the cart as a tensor."""
        screen = self.env.render(mode='rgb_array').transpose((2, 0, 1))  # torch order (CHW)

        ## Strip off top and bottom
        screen = screen[:, 320:640]
        view_width = 640
        cart_location = self.get_cart_location()

        if cart_location < view_width // 2:  # left edge zone
            slice_range = slice(view_width)
        elif cart_location > (self.SCREEN_WIDTH - view_width // 2):  # right edge zone
            slice_range = slice(-view_width, None)
        else:  # middle zone
            slice_range = slice(cart_location - view_width // 2,
                                cart_location + view_width // 2)

        ## Crop sides
        screen = screen[:, :, slice_range]

        ## reformat, normalize color values
        screen = np.ascontiguousarray(screen, dtype=np.float32) / 255
        screen = torch.from_numpy(screen)
        return self.RESIZE(screen).unsqueeze(0).to(self.device)
