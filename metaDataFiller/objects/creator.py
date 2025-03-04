class Creator:
    existingCreatorUrls = []
    newCreatorUrls = []

    def __init__(self):
        self.creatorId = "None"
        self.existingCreatorUrls = []
        self.newCreatorUrls = []
        self.creatorName = "None"

    def __ne__(self, other):
        return (self.creatorId != other.creatorId or
                self.existingCreatorUrls != other.existingCreatorUrls or
                self.newCreatorUrls != other.newCreatorUrls or
                self.creatorName != other.creatorName)

    def existing_creator(self, creator):
        self.creatorId = creator.creatorId
        self.existingCreatorUrls = creator.existingCreatorUrls
        self.newCreatorUrls = creator.newCreatorUrls
        self.creatorName = creator.creatorName
