"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { ArrowLeft, Eye, Users, Gavel, Calendar } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"

const biddingHistory = [
  {
    bidder: "Christina Brooks",
    bidderId: "00001",
    avatar: "CB",
    amount: 12500,
    bids: 5,
    time: "2024-01-20 14:30",
    status: "winning",
  },
  {
    bidder: "Michael Johnson",
    bidderId: "00002",
    avatar: "MJ",
    amount: 11800,
    bids: 3,
    time: "2024-01-20 14:25",
    status: "outbid",
  },
  {
    bidder: "Sarah Wilson",
    bidderId: "00003",
    avatar: "SW",
    amount: 11200,
    bids: 4,
    time: "2024-01-20 14:20",
    status: "outbid",
  },
  {
    bidder: "David Chen",
    bidderId: "00004",
    avatar: "DC",
    amount: 10500,
    bids: 2,
    time: "2024-01-20 14:15",
    status: "outbid",
  },
]

export default function AuctionDetails() {
  const router = useRouter()
  const [timeRemaining, setTimeRemaining] = useState({
    days: 0,
    hours: 2,
    minutes: 15,
    seconds: 30,
  })

  // Countdown timer effect
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeRemaining((prev) => {
        let { days, hours, minutes, seconds } = prev

        if (seconds > 0) {
          seconds--
        } else if (minutes > 0) {
          minutes--
          seconds = 59
        } else if (hours > 0) {
          hours--
          minutes = 59
          seconds = 59
        } else if (days > 0) {
          days--
          hours = 23
          minutes = 59
          seconds = 59
        }

        return { days, hours, minutes, seconds }
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  const handleCustomerClick = (customerId: string) => {
    router.push(`/customers/${customerId}`)
  }

  const formatTime = (value: number) => {
    return value.toString().padStart(2, "0")
  }

  const isAuctionEnded =
    timeRemaining.days === 0 && timeRemaining.hours === 0 && timeRemaining.minutes === 0 && timeRemaining.seconds === 0

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/products">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="w-4 h-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-2xl font-bold">Auction Details</h1>
          <div className="text-sm text-gray-500">Home &gt; Auctions &gt; Luxury Beachfront Villa - Santorini</div>
        </div>
        <Badge className={isAuctionEnded ? "bg-red-100 text-red-800 ml-auto" : "bg-green-100 text-green-800 ml-auto"}>
          {isAuctionEnded ? "Ended" : "Active"}
        </Badge>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Property Image */}
          <Card>
            <CardContent className="p-0">
              <div className="relative">
                <div className="bg-gray-100 rounded-t-lg h-64 flex items-center justify-center">
                  <div className="text-center text-gray-400">
                    <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-2">
                      <span className="text-2xl">📷</span>
                    </div>
                    <p>Luxury Villa</p>
                  </div>
                </div>
                <div className="absolute top-4 right-4 bg-white px-2 py-1 rounded-lg shadow">
                  <div className="flex items-center gap-1">
                    <Eye className="w-4 h-4" />
                    <span className="text-sm font-medium">1250 views</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Property Details */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-2xl font-bold mb-4">Luxury Beachfront Villa - Santorini</h2>
              <div className="flex items-center gap-2 text-gray-600 mb-4">
                <span>📍 Santorini, Greece</span>
              </div>
              <p className="text-gray-600">
                Stunning 5-bedroom villa with panoramic ocean views, private beach access, infinity pool, and modern
                amenities. Perfect for luxury vacation rentals or private residence.
              </p>
            </CardContent>
          </Card>

          {/* Bidding History */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Gavel className="w-5 h-5" />
                Bidding History (28 bids)
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {biddingHistory.map((bid, index) => (
                <div
                  key={index}
                  className={`flex items-center justify-between p-4 rounded-lg ${
                    bid.status === "winning" ? "bg-green-50 border border-green-200" : "bg-gray-50"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Avatar
                      className="w-10 h-10 cursor-pointer hover:ring-2 hover:ring-blue-500 transition-all"
                      onClick={() => handleCustomerClick(bid.bidderId)}
                    >
                      <AvatarImage src="/placeholder-user.jpg" />
                      <AvatarFallback>{bid.avatar}</AvatarFallback>
                    </Avatar>
                    <div>
                      <div
                        className="font-medium cursor-pointer hover:text-blue-600 transition-colors"
                        onClick={() => handleCustomerClick(bid.bidderId)}
                      >
                        {bid.bidder}
                      </div>
                      <div className="text-sm text-gray-500">
                        {bid.bids} bids • {bid.time}
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xl font-bold">${bid.amount.toLocaleString()}</div>
                    {bid.status === "winning" && <Badge className="bg-green-100 text-green-800">Winning Bid</Badge>}
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Current Auction Status */}
          <Card>
            <CardHeader>
              <CardTitle>Current Auction Status</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="text-sm text-gray-600">Current Highest Bid</div>
                <div className="text-2xl font-bold text-green-600">$12,500</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Starting Price</div>
                <div className="text-lg font-medium">$5,000</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Reserve Price</div>
                <div className="text-lg font-medium">$15,000</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Time Remaining</div>
                {isAuctionEnded ? (
                  <div className="text-lg font-medium text-red-600">Auction Ended</div>
                ) : (
                  <div className="grid grid-cols-4 gap-2 mt-2">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-orange-600">{formatTime(timeRemaining.days)}</div>
                      <div className="text-xs text-gray-500">Days</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-orange-600">{formatTime(timeRemaining.hours)}</div>
                      <div className="text-xs text-gray-500">Hours</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-orange-600">{formatTime(timeRemaining.minutes)}</div>
                      <div className="text-xs text-gray-500">Minutes</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-orange-600">{formatTime(timeRemaining.seconds)}</div>
                      <div className="text-xs text-gray-500">Seconds</div>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Auction Statistics */}
          <Card>
            <CardHeader>
              <CardTitle>Auction Statistics</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4 text-blue-500" />
                  <span className="text-gray-600">Total Bidders</span>
                </div>
                <span className="font-medium">12</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Gavel className="w-4 h-4 text-purple-500" />
                  <span className="text-gray-600">Total Bids</span>
                </div>
                <span className="font-medium">28</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Eye className="w-4 h-4 text-green-500" />
                  <span className="text-gray-600">Views</span>
                </div>
                <span className="font-medium">1250</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-orange-500" />
                  <span className="text-gray-600">Started</span>
                </div>
                <span className="font-medium">2024-01-20 10:00</span>
              </div>
            </CardContent>
          </Card>

          {/* Winner Information (if auction ended) */}
          {isAuctionEnded && (
            <Card>
              <CardHeader>
                <CardTitle>Auction Winner</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-3 p-4 bg-green-50 rounded-lg">
                  <Avatar
                    className="w-12 h-12 cursor-pointer hover:ring-2 hover:ring-blue-500 transition-all"
                    onClick={() => handleCustomerClick("00001")}
                  >
                    <AvatarImage src="/placeholder-user.jpg" />
                    <AvatarFallback>CB</AvatarFallback>
                  </Avatar>
                  <div className="flex-1">
                    <div
                      className="font-medium cursor-pointer hover:text-blue-600 transition-colors"
                      onClick={() => handleCustomerClick("00001")}
                    >
                      Christina Brooks
                    </div>
                    <div className="text-sm text-gray-500">Winning bid: $12,500</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
