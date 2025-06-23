"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  ArrowLeft,
  MapPin,
  Bed,
  Bath,
  Maximize,
  Gavel,
  Check,
  X,
  FolderPlus,
  Wifi,
  Car,
  Utensils,
  Waves,
  Dumbbell,
  Wind,
  Star,
  Users,
  Heart,
  Share,
  Flag,
} from "lucide-react"
import Link from "next/link"
import { useParams } from "next/navigation"
import { useToast } from "@/hooks/use-toast"
import { ApproveModal } from "@/components/modals/approve-modal"
import { RejectModal } from "@/components/modals/reject-modal"
import { AddToCatalogModal } from "@/components/modals/add-to-catalog-modal"

const propertyImages = [
  "/placeholder.svg?height=400&width=600",
  "/placeholder.svg?height=300&width=400",
  "/placeholder.svg?height=300&width=400",
  "/placeholder.svg?height=300&width=400",
  "/placeholder.svg?height=300&width=400",
]

const amenities = [
  { icon: Wifi, label: "Free WiFi" },
  { icon: Car, label: "Free Parking" },
  { icon: Utensils, label: "Full Kitchen" },
  { icon: Waves, label: "Private Pool" },
  { icon: Dumbbell, label: "Gym Access" },
  { icon: Wind, label: "Air Conditioning" },
]

const reviews = [
  {
    id: 1,
    user: "Sarah Johnson",
    avatar: "SJ",
    rating: 5,
    date: "March 2024",
    comment:
      "Absolutely stunning villa with breathtaking ocean views. The infinity pool was perfect for relaxing after exploring Santorini. Highly recommend!",
  },
  {
    id: 2,
    user: "Michael Chen",
    avatar: "MC",
    rating: 5,
    date: "February 2024",
    comment:
      "Perfect location and amazing amenities. The villa exceeded our expectations. Great for families and the host was very responsive.",
  },
  {
    id: 3,
    user: "Emma Wilson",
    avatar: "EW",
    rating: 4,
    date: "January 2024",
    comment:
      "Beautiful property with modern amenities. The sunset views from the terrace are unforgettable. Minor issue with WiFi but overall excellent stay.",
  },
]

export default function ProductDetail() {
  const params = useParams()
  const [selectedImage, setSelectedImage] = useState(0)

  const [approveModal, setApproveModal] = useState({
    open: false,
    productId: params.id as string,
    productName: "5-Bedroom Villa with Private Pool",
  })
  const [rejectModal, setRejectModal] = useState({
    open: false,
    productId: params.id as string,
    productName: "5-Bedroom Villa with Private Pool",
  })
  const [catalogModal, setCatalogModal] = useState({
    open: false,
    productId: params.id as string,
    productName: "5-Bedroom Villa with Private Pool",
  })
  const { toast } = useToast()

  const handleApprove = () => {
    setApproveModal((prev) => ({ ...prev, open: true }))
  }

  const handleReject = () => {
    setRejectModal((prev) => ({ ...prev, open: true }))
  }

  const handleAddToCatalog = () => {
    setCatalogModal((prev) => ({ ...prev, open: true }))
  }

  const onApproveConfirm = (note?: string) => {
    toast({
      title: "Product Approved",
      description: `Product has been approved successfully.`,
    })
  }

  const onRejectConfirm = (reason: string, note?: string) => {
    toast({
      title: "Product Rejected",
      description: `Product has been rejected. Reason: ${reason}`,
      variant: "destructive",
    })
  }

  const onCatalogConfirm = (category: string, featured: boolean) => {
    toast({
      title: "Added to Catalog",
      description: `Product has been added to ${category} catalog${featured ? " as featured" : ""}.`,
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/products">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="w-4 h-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-2xl font-bold">Product Detail</h1>
          <div className="text-sm text-gray-500">Home &gt; Products &gt; Product Detail</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Property Header */}
          <div className="space-y-4">
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-3xl font-bold">5-Bedroom Villa with Private Pool</h2>
                <div className="flex items-center gap-2 mt-2 text-gray-600">
                  <MapPin className="w-4 h-4" />
                  <span>Santorini, Greece</span>
                  <span>•</span>
                  <div className="flex items-center gap-1">
                    <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                    <span className="font-medium">4.9</span>
                    <span>(127 reviews)</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="outline" size="sm">
                  <Share className="w-4 h-4 mr-2" />
                  Share
                </Button>
                <Button variant="outline" size="sm">
                  <Heart className="w-4 h-4 mr-2" />
                  Save
                </Button>
                <Button variant="outline" size="sm">
                  <Flag className="w-4 h-4 mr-2" />
                  Report
                </Button>
              </div>
            </div>
          </div>

          {/* Image Gallery */}
          <div className="grid grid-cols-4 gap-2 h-96">
            <div className="col-span-2 row-span-2">
              <img
                src={propertyImages[selectedImage] || "/placeholder.svg"}
                alt="Main property image"
                className="w-full h-full object-cover rounded-lg cursor-pointer"
                onClick={() => setSelectedImage(0)}
              />
            </div>
            {propertyImages.slice(1, 5).map((image, index) => (
              <div key={index} className="relative">
                <img
                  src={image || "/placeholder.svg"}
                  alt={`Property image ${index + 2}`}
                  className="w-full h-full object-cover rounded-lg cursor-pointer hover:opacity-80 transition-opacity"
                  onClick={() => setSelectedImage(index + 1)}
                />
                {index === 3 && (
                  <div className="absolute inset-0 bg-black bg-opacity-50 rounded-lg flex items-center justify-center">
                    <span className="text-white font-medium">+12 photos</span>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Property Details */}
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-semibold mb-4">About this place</h3>
              <p className="text-gray-600 leading-relaxed">
                Stunning luxury villa with panoramic ocean views, private beach access, infinity pool, and modern
                amenities. Perfect for luxury vacation rentals or private residence. This exceptional property features
                spacious living areas, fully equipped gourmet kitchen, and beautiful outdoor spaces with breathtaking
                sea views.
              </p>
              <p className="text-gray-600 leading-relaxed mt-4">
                Located in the heart of Santorini, this villa offers the perfect blend of traditional Greek architecture
                and modern luxury. Wake up to stunning sunrises over the Aegean Sea and enjoy unforgettable sunsets from
                your private terrace.
              </p>
            </div>

            <Separator />

            {/* Property Features */}
            <div>
              <h3 className="text-xl font-semibold mb-4">Property Features</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="flex items-center gap-2">
                  <Bed className="w-5 h-5 text-gray-500" />
                  <span>5 bedrooms</span>
                </div>
                <div className="flex items-center gap-2">
                  <Bath className="w-5 h-5 text-gray-500" />
                  <span>4 bathrooms</span>
                </div>
                <div className="flex items-center gap-2">
                  <Maximize className="w-5 h-5 text-gray-500" />
                  <span>250 m²</span>
                </div>
                <div className="flex items-center gap-2">
                  <Users className="w-5 h-5 text-gray-500" />
                  <span>Up to 10 guests</span>
                </div>
              </div>
            </div>

            <Separator />

            {/* Amenities */}
            <div>
              <h3 className="text-xl font-semibold mb-4">Amenities</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {amenities.map((amenity, index) => (
                  <div key={index} className="flex items-center gap-3">
                    <amenity.icon className="w-5 h-5 text-gray-500" />
                    <span>{amenity.label}</span>
                  </div>
                ))}
              </div>
            </div>

            <Separator />

            {/* Host Information */}
            <div>
              <h3 className="text-xl font-semibold mb-4">Meet your host</h3>
              <div className="flex items-start gap-4 p-4 border rounded-lg">
                <Avatar className="w-16 h-16">
                  <AvatarImage src="/placeholder-user.jpg" />
                  <AvatarFallback>CB</AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h4 className="font-semibold text-lg">Christina Brooks</h4>
                    <Badge className="bg-blue-100 text-blue-800">Superhost</Badge>
                  </div>
                  <div className="text-sm text-gray-600 space-y-1">
                    <div>⭐ 4.9 rating • 127 reviews</div>
                    <div>📅 Hosting since 2019</div>
                    <div>🏆 Verified host</div>
                  </div>
                  <p className="text-gray-600 mt-3">
                    I'm passionate about providing exceptional experiences for my guests. I love sharing the beauty of
                    Santorini and ensuring every stay is memorable.
                  </p>
                </div>
              </div>
            </div>

            <Separator />

            {/* Reviews */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-semibold">Reviews</h3>
                <div className="flex items-center gap-2">
                  <Star className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                  <span className="font-semibold">4.9</span>
                  <span className="text-gray-500">• 127 reviews</span>
                </div>
              </div>

              <div className="space-y-4">
                {reviews.map((review) => (
                  <div key={review.id} className="border-b pb-4 last:border-b-0">
                    <div className="flex items-start gap-3">
                      <Avatar className="w-10 h-10">
                        <AvatarImage src="/placeholder-user.jpg" />
                        <AvatarFallback>{review.avatar}</AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-medium">{review.user}</span>
                          <span className="text-gray-500 text-sm">{review.date}</span>
                        </div>
                        <div className="flex items-center gap-1 mb-2">
                          {[...Array(review.rating)].map((_, i) => (
                            <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                          ))}
                        </div>
                        <p className="text-gray-600">{review.comment}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <Button variant="outline" className="mt-4">
                Show all 127 reviews
              </Button>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Link href={`/auctions/${params.id}`}>
                <Button className="w-full bg-blue-500 hover:bg-blue-600">
                  <Gavel className="w-4 h-4 mr-2" />
                  View Auction
                </Button>
              </Link>
              <Button
                variant="outline"
                className="w-full bg-green-50 text-green-700 border-green-200 hover:bg-green-100"
                onClick={handleApprove}
              >
                <Check className="w-4 h-4 mr-2" />
                Approve Product
              </Button>
              <Button
                variant="outline"
                className="w-full bg-red-50 text-red-700 border-red-200 hover:bg-red-100"
                onClick={handleReject}
              >
                <X className="w-4 h-4 mr-2" />
                Reject Product
              </Button>
              <Button
                variant="outline"
                className="w-full bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100"
                onClick={handleAddToCatalog}
              >
                <FolderPlus className="w-4 h-4 mr-2" />
                Add to Catalog
                <Badge className="ml-2 bg-blue-500 text-white">1</Badge>
              </Button>
            </CardContent>
          </Card>

          {/* Property Statistics */}
          <Card>
            <CardHeader>
              <CardTitle>Property Statistics</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Listed Date</span>
                <span className="font-medium">Feb 14, 2019</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Starting Price</span>
                <span className="font-medium">$200/night</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Total Views</span>
                <span className="font-medium">1,250</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Saved by</span>
                <span className="font-medium">89 users</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Response Rate</span>
                <span className="font-medium">98%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Response Time</span>
                <span className="font-medium">Within 1 hour</span>
              </div>
            </CardContent>
          </Card>

          {/* Pricing Information */}
          <Card>
            <CardHeader>
              <CardTitle>Pricing Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Base Price</span>
                <span className="font-medium">$200/night</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Cleaning Fee</span>
                <span className="font-medium">$50</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Service Fee</span>
                <span className="font-medium">$25</span>
              </div>
              <Separator />
              <div className="flex items-center justify-between font-semibold">
                <span>Total per night</span>
                <span>$275</span>
              </div>
            </CardContent>
          </Card>

          {/* Location */}
          <Card>
            <CardHeader>
              <CardTitle>Location</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center mb-4">
                <span className="text-gray-500">Map placeholder</span>
              </div>
              <div className="space-y-2">
                <div className="font-medium">Santorini, Greece</div>
                <div className="text-sm text-gray-600">
                  Located in the picturesque village of Oia, famous for its stunning sunsets and traditional
                  architecture.
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
      <ApproveModal
        open={approveModal.open}
        onOpenChange={(open) => setApproveModal((prev) => ({ ...prev, open }))}
        productName={approveModal.productName}
        onConfirm={onApproveConfirm}
      />

      <RejectModal
        open={rejectModal.open}
        onOpenChange={(open) => setRejectModal((prev) => ({ ...prev, open }))}
        productName={rejectModal.productName}
        onConfirm={onRejectConfirm}
      />

      <AddToCatalogModal
        open={catalogModal.open}
        onOpenChange={(open) => setCatalogModal((prev) => ({ ...prev, open }))}
        productName={catalogModal.productName}
        onConfirm={onCatalogConfirm}
      />
    </div>
  )
}
