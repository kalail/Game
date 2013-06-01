import PAL


class AssetManager(object):
    """Asset Manager

    Loads assets used by a level and provide the engine access to them.

    """

    extensions = {
        'audio': [
            'ogg',
            'wav',
        ],
        'image': [
            'jpg',
            'jpeg',
            'png',
        ]
    }

    @staticmethod
    def allowed_extensions():
        """Return a list of allowed extensions."""
        exts = []
        for category in AssetManager.extensions:
            exts.extend(AssetManager.extensions[category])
        return exts

    @staticmethod
    def create_manifest(assets):
        manifest = []
        for asset in assets:
            for cat in AssetManager.extensions:
                for ext in AssetManager.extensions[cat]:
                    if asset.endswith(ext):
                        manifest.append((asset, cat, ext))
        if len(manifest) != len(assets):
            raise Exception('Error creating manifest')
        return manifest


    def __init__(self, assets):
        """Save asset list and set up internal data structures."""
        # Create unique list by converting to a set.
        unique_assets = list(set(assets))
        # Check for allowed extensions
        allowed = AssetManager.allowed_extensions()
        for a in unique_assets:
            check_list = [True if a.endswith(ext) else False for ext in allowed]
            if True not in check_list:
                raise Exception('Unsupported asset extension type.')
        self.manifest = AssetManager.create_manifest(unique_assets)
        self.assets = {}

    def load(self):
        """Load assets saved in asset list. Checks for duplicates and allowed extensions."""
        for order in self.manifest:
            cat = order[1]
            path = order[0]
            if cat == 'image':
                asset = PAL.load_image(path)
            elif cat == 'audio':
                asset = PAL.load_sound(path)
            else:
                raise Exception('Unsupported asset type.')
            self.assets[path] = asset

    def get(self, asset):
        return self.assets[asset]