package models;

class Player {
  private String name;
  private int color;

  Player(String name, int color) {
    this.name = name;
    this.color = color;
  }

  String getName() {
    return name;
  }

  int getColor() {
    return color;
  }
}
