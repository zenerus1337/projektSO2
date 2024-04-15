import pygame as pg

class World():
    def __init__(self, data, map_image):
        self.waypoints = []
        self.level_data = data
        self.image = map_image
    
    def process_data(self):
        #zbieranie informacji o ścieżce z pliku
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                for obj in layer ["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)

                    
    def process_waypoints(self,data):
        #pozyskiwanie współrzędnych x i y przez poruszanie się przez liste
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            self.waypoints.append((temp_x,temp_y))

    def draw(self,surface):
        surface.blit(self.image, (0,0))
