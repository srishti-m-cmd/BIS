const mongoose = require("mongoose");

const placeGeoSchema = new mongoose.Schema(
  {
    placeId: { type: Number, required: true, unique: true },
    name: { type: String, required: true },
    rating: { type: Number, default: 0 },
    reviewCount: { type: Number, default: 0 },
    address: { type: String, default: "" },
    hashtag: { type: String, default: "" },
    wifi: { type: Boolean, default: false },
    indoor: { type: Boolean, default: false },
    outdoor: { type: Boolean, default: false },
    location: {
      type: {
        type: String,
        enum: ["Point"],
        default: "Point",
      },
      coordinates: {
        type: [Number],
        required: true,
      },
    },
  },
  { timestamps: true },
);

placeGeoSchema.index({ location: "2dsphere" });

module.exports = mongoose.model("PlaceGeo", placeGeoSchema);
