"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import {
  ArrowLeft,
  MessageSquare,
  Edit,
  UserX,
  Eye,
  Download,
  DollarSign,
  Calendar,
  MapPin,
  Phone,
  CreditCard,
  TrendingUp,
  Activity,
  Clock,
  CheckCircle,
  AlertTriangle,
} from "lucide-react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { useToast } from "@/hooks/use-toast"

const propertyListings = [
  {
    id: "PROP001",
    name: "Luxury Beachfront Villa - Malibu",
    category: "Luxury Villa",
    startingPrice: 5000,
    finalPrice: 8500,
    status: "Completed",
    views: 1250,
    bids: 23,
  },
  {
    id: "PROP002",
    name: "Mountain Cabin - Aspen",
    category: "Mountain Cabin",
    startingPrice: 3000,
    finalPrice: 4200,
    status: "Completed",
    views: 890,
    bids: 15,
  },
  {
    id: "PROP003",
    name: "City Penthouse",
    category: "City Apartment",
    startingPrice: 8000,
    finalPrice: null,
    status: "Active",
    views: 456,
    bids: 8,
  },
]

const biddingHistory = [
  {
    id: "BID001",
    property: "Luxury Beachfront Villa - Malibu",
    bidAmount: 8500,
    bidTime: "2024-01-20 14:30",
    status: "Won",
    maxBid: 9000,
  },
  {
    id: "BID002",
    property: "Mountain Cabin - Aspen",
    bidAmount: 4200,
    bidTime: "2024-01-19 16:45",
    status: "Won",
    maxBid: 4500,
  },
  {
    id: "BID003",
    property: "City Penthouse",
    bidAmount: 7800,
    bidTime: "2024-01-21 10:15",
    status: "Outbid",
    maxBid: 8200,
  },
  {
    id: "BID004",
    property: "Beach House Miami",
    bidAmount: 6500,
    bidTime: "2024-01-18 12:00",
    status: "Lost",
    maxBid: 7000,
  },
  {
    id: "BID005",
    property: "Downtown Loft",
    bidAmount: 3200,
    bidTime: "2024-01-17 09:30",
    status: "Won",
    maxBid: 3500,
  },
]

const paymentHistory = [
  {
    id: "PAY001",
    property: "Luxury Beachfront Villa - Malibu",
    amount: 8500,
    date: "2024-01-21",
    method: "Credit Card",
    status: "Completed",
    transactionId: "TXN123456789",
  },
  {
    id: "PAY002",
    property: "Mountain Cabin - Aspen",
    amount: 4200,
    date: "2024-01-20",
    method: "Bank Transfer",
    status: "Completed",
    transactionId: "TXN123456788",
  },
  {
    id: "PAY003",
    property: "Beach House Miami",
    amount: 500,
    date: "2024-01-18",
    method: "Credit Card",
    status: "Refunded",
    transactionId: "TXN123456787",
  },
  {
    id: "PAY004",
    property: "Downtown Loft",
    amount: 3200,
    date: "2024-01-17",
    method: "PayPal",
    status: "Completed",
    transactionId: "TXN123456786",
  },
  {
    id: "PAY005",
    property: "Suburban House",
    amount: 2800,
    date: "2024-01-15",
    method: "Credit Card",
    status: "Pending",
    transactionId: "TXN123456785",
  },
]

const activityLog = [
  {
    id: "ACT001",
    action: "Won auction",
    description: "Won auction for Luxury Beachfront Villa - Malibu",
    timestamp: "2024-01-20 14:30",
    type: "auction",
  },
  {
    id: "ACT002",
    action: "Payment completed",
    description: "Payment of $8,500 completed for Luxury Beachfront Villa",
    timestamp: "2024-01-21 09:15",
    type: "payment",
  },
  {
    id: "ACT003",
    action: "Profile updated",
    description: "Updated contact information",
    timestamp: "2024-01-19 16:20",
    type: "profile",
  },
  {
    id: "ACT004",
    action: "Bid placed",
    description: "Placed bid of $7,800 on City Penthouse",
    timestamp: "2024-01-21 10:15",
    type: "bid",
  },
  {
    id: "ACT005",
    action: "Account verified",
    description: "Email and phone number verified",
    timestamp: "2024-01-15 14:00",
    type: "verification",
  },
]

export default function CustomerProfile() {
  const [activeTab, setActiveTab] = useState("overview")
  const [messageModal, setMessageModal] = useState(false)
  const [editModal, setEditModal] = useState(false)
  const [suspendModal, setSuspendModal] = useState(false)
  const [viewPropertyModal, setViewPropertyModal] = useState({ open: false, property: null as any })
  const [viewBidModal, setViewBidModal] = useState({ open: false, bid: null as any })
  const [viewPaymentModal, setViewPaymentModal] = useState({ open: false, payment: null as any })
  const [message, setMessage] = useState("")
  const [editForm, setEditForm] = useState({
    name: "Christina Brooks",
    email: "christina.brooks@example.com",
    phone: "+1 (555) 123-4567",
    address: "089 Kutch Green Apt. 448, New York, NY 10001",
  })

  const router = useRouter()
  const { toast } = useToast()

  // Handle view actions cho các tab
  const handleViewProperty = (property: any) => {
    setViewPropertyModal({ open: true, property })
  }

  const handleViewBid = (bid: any) => {
    setViewBidModal({ open: true, bid })
  }

  const handleViewPayment = (payment: any) => {
    setViewPaymentModal({ open: true, payment })
  }

  const handleDownloadReport = (type: string, id: string) => {
    toast({
      title: "Download Started",
      description: `Downloading ${type} report for ${id}...`,
    })
  }

  const handleSendMessage = () => {
    if (!message.trim()) {
      toast({
        title: "Error",
        description: "Please enter a message.",
        variant: "destructive",
      })
      return
    }

    toast({
      title: "Message Sent",
      description: "Your message has been sent to Christina Brooks.",
    })
    setMessageModal(false)
    setMessage("")
  }

  const handleEditProfile = () => {
    toast({
      title: "Profile Updated",
      description: "Customer profile has been updated successfully.",
    })
    setEditModal(false)
  }

  const handleSuspend = () => {
    toast({
      title: "Account Suspended",
      description: "Christina Brooks' account has been suspended.",
      variant: "destructive",
    })
    setSuspendModal(false)
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "Completed":
      case "Won":
        return <Badge className="bg-green-100 text-green-800">{status}</Badge>
      case "Active":
        return <Badge className="bg-blue-100 text-blue-800">{status}</Badge>
      case "Outbid":
      case "Lost":
        return <Badge className="bg-red-100 text-red-800">{status}</Badge>
      case "Pending":
        return <Badge className="bg-yellow-100 text-yellow-800">{status}</Badge>
      case "Refunded":
        return <Badge className="bg-gray-100 text-gray-800">{status}</Badge>
      default:
        return <Badge variant="outline">{status}</Badge>
    }
  }

  const getActivityIcon = (type: string) => {
    switch (type) {
      case "auction":
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case "payment":
        return <DollarSign className="w-4 h-4 text-blue-500" />
      case "profile":
        return <Edit className="w-4 h-4 text-purple-500" />
      case "bid":
        return <TrendingUp className="w-4 h-4 text-orange-500" />
      case "verification":
        return <CheckCircle className="w-4 h-4 text-green-500" />
      default:
        return <Activity className="w-4 h-4 text-gray-500" />
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href="/customers">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-4 h-4" />
            </Button>
          </Link>
          <div>
            <h1 className="text-2xl font-bold">Customer Profile</h1>
            <div className="text-sm text-gray-500">Home &gt; Customers &gt; Christina Brooks</div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={() => setMessageModal(true)}>
            <MessageSquare className="w-4 h-4 mr-2" />
            Send Message
          </Button>
          <Button variant="outline" onClick={() => setEditModal(true)}>
            <Edit className="w-4 h-4 mr-2" />
            Edit Profile
          </Button>
          <Button variant="destructive" onClick={() => setSuspendModal(true)}>
            <UserX className="w-4 h-4 mr-2" />
            Suspend
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Customer Info Sidebar */}
        <div className="lg:col-span-1">
          <Card>
            <CardContent className="p-6 space-y-6">
              <div className="text-center">
                <Avatar className="w-24 h-24 mx-auto mb-4">
                  <AvatarImage src="/placeholder-user.jpg" />
                  <AvatarFallback>CB</AvatarFallback>
                </Avatar>
                <h2 className="text-xl font-bold">Christina Brooks</h2>
                <p className="text-gray-500">christina.brooks@example.com</p>
                <div className="flex items-center justify-center gap-2 mt-2">
                  <Badge className="bg-purple-100 text-purple-800">VIP</Badge>
                  <Badge className="bg-green-100 text-green-800">Verified</Badge>
                </div>
              </div>

              <Separator />

              <div className="space-y-4">
                <div>
                  <h3 className="font-medium text-gray-600 flex items-center gap-2">
                    <Phone className="w-4 h-4" />
                    Contact
                  </h3>
                  <p className="text-sm">+1 (555) 123-4567</p>
                  <p className="text-sm text-gray-500 flex items-start gap-2 mt-1">
                    <MapPin className="w-4 h-4 mt-0.5" />
                    089 Kutch Green Apt. 448, New York, NY 10001
                  </p>
                </div>

                <div>
                  <h3 className="font-medium text-gray-600 flex items-center gap-2">
                    <Calendar className="w-4 h-4" />
                    Member Since
                  </h3>
                  <p className="text-sm">14 Feb 2019</p>
                </div>

                <div>
                  <h3 className="font-medium text-gray-600 flex items-center gap-2">
                    <Clock className="w-4 h-4" />
                    Last Activity
                  </h3>
                  <p className="text-sm">2 hours ago</p>
                </div>

                <div>
                  <h3 className="font-medium text-gray-600 flex items-center gap-2">
                    <CreditCard className="w-4 h-4" />
                    Credit Score
                  </h3>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div className="bg-green-500 h-2 rounded-full" style={{ width: "85%" }}></div>
                    </div>
                    <span className="text-sm font-medium">850</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3">
          <Card>
            {/* Tabs */}
            <div className="flex space-x-8 border-b px-6 py-4">
              <button
                className={`pb-2 ${
                  activeTab === "overview"
                    ? "border-b-2 border-blue-500 text-blue-600 font-medium"
                    : "text-gray-500 hover:text-gray-700"
                }`}
                onClick={() => setActiveTab("overview")}
              >
                Overview
              </button>
              <button
                className={`pb-2 ${
                  activeTab === "listings"
                    ? "border-b-2 border-blue-500 text-blue-600 font-medium"
                    : "text-gray-500 hover:text-gray-700"
                }`}
                onClick={() => setActiveTab("listings")}
              >
                Property Listings (3)
              </button>
              <button
                className={`pb-2 ${
                  activeTab === "bidding"
                    ? "border-b-2 border-blue-500 text-blue-600 font-medium"
                    : "text-gray-500 hover:text-gray-700"
                }`}
                onClick={() => setActiveTab("bidding")}
              >
                Bidding History (5)
              </button>
              <button
                className={`pb-2 ${
                  activeTab === "payment"
                    ? "border-b-2 border-blue-500 text-blue-600 font-medium"
                    : "text-gray-500 hover:text-gray-700"
                }`}
                onClick={() => setActiveTab("payment")}
              >
                Payment History (5)
              </button>
              <button
                className={`pb-2 ${
                  activeTab === "activity"
                    ? "border-b-2 border-blue-500 text-blue-600 font-medium"
                    : "text-gray-500 hover:text-gray-700"
                }`}
                onClick={() => setActiveTab("activity")}
              >
                Activity Log
              </button>
            </div>

            <div className="p-6">
              {/* Overview Tab */}
              {activeTab === "overview" && (
                <div className="space-y-6">
                  <h3 className="text-lg font-bold">Customer Overview</h3>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <Card>
                      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Spent</CardTitle>
                        <DollarSign className="w-4 h-4 text-green-500" />
                      </CardHeader>
                      <CardContent>
                        <div className="text-2xl font-bold text-green-600">$15,750</div>
                        <p className="text-xs text-gray-500">+12% from last month</p>
                      </CardContent>
                    </Card>

                    <Card>
                      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Auctions Won</CardTitle>
                        <TrendingUp className="w-4 h-4 text-blue-500" />
                      </CardHeader>
                      <CardContent>
                        <div className="text-2xl font-bold">8</div>
                        <p className="text-xs text-gray-500">85% win rate</p>
                      </CardContent>
                    </Card>

                    <Card>
                      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Active Bids</CardTitle>
                        <Activity className="w-4 h-4 text-orange-500" />
                      </CardHeader>
                      <CardContent>
                        <div className="text-2xl font-bold">3</div>
                        <p className="text-xs text-gray-500">2 leading</p>
                      </CardContent>
                    </Card>
                  </div>

                  <div>
                    <h4 className="font-semibold mb-3">Recent Activity</h4>
                    <div className="space-y-3">
                      {activityLog.slice(0, 3).map((activity) => (
                        <div key={activity.id} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                          {getActivityIcon(activity.type)}
                          <div className="flex-1">
                            <div className="font-medium">{activity.action}</div>
                            <div className="text-sm text-gray-600">{activity.description}</div>
                            <div className="text-xs text-gray-400">{activity.timestamp}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Property Listings Tab */}
              {activeTab === "listings" && (
                <div>
                  <h3 className="text-lg font-bold mb-4">Property Listings</h3>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>PROPERTY</TableHead>
                        <TableHead>CATEGORY</TableHead>
                        <TableHead>STARTING PRICE</TableHead>
                        <TableHead>FINAL PRICE</TableHead>
                        <TableHead>STATUS</TableHead>
                        <TableHead>PERFORMANCE</TableHead>
                        <TableHead>ACTIONS</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {propertyListings.map((property) => (
                        <TableRow key={property.id}>
                          <TableCell>
                            <div className="flex items-center gap-3">
                              <div className="w-12 h-12 bg-gray-200 rounded"></div>
                              <div>
                                <div className="font-medium">{property.name}</div>
                                <div className="text-sm text-gray-500">ID: {property.id}</div>
                              </div>
                            </div>
                          </TableCell>
                          <TableCell>{property.category}</TableCell>
                          <TableCell>${property.startingPrice.toLocaleString()}</TableCell>
                          <TableCell>
                            {property.finalPrice ? (
                              <span className="font-medium text-green-600">
                                ${property.finalPrice.toLocaleString()}
                              </span>
                            ) : (
                              "-"
                            )}
                          </TableCell>
                          <TableCell>{getStatusBadge(property.status)}</TableCell>
                          <TableCell>
                            <div className="text-sm">
                              <div>{property.views} views</div>
                              <div className="text-gray-500">{property.bids} bids</div>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-2">
                              <Button size="sm" variant="outline" onClick={() => handleViewProperty(property)}>
                                <Eye className="w-4 h-4" />
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => handleDownloadReport("property", property.id)}
                              >
                                <Download className="w-4 h-4" />
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              )}

              {/* Bidding History Tab */}
              {activeTab === "bidding" && (
                <div>
                  <h3 className="text-lg font-bold mb-4">Bidding History</h3>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>PROPERTY</TableHead>
                        <TableHead>BID AMOUNT</TableHead>
                        <TableHead>MAX BID</TableHead>
                        <TableHead>BID TIME</TableHead>
                        <TableHead>STATUS</TableHead>
                        <TableHead>ACTIONS</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {biddingHistory.map((bid) => (
                        <TableRow key={bid.id}>
                          <TableCell>
                            <div className="font-medium">{bid.property}</div>
                            <div className="text-sm text-gray-500">ID: {bid.id}</div>
                          </TableCell>
                          <TableCell>
                            <span className="font-medium">${bid.bidAmount.toLocaleString()}</span>
                          </TableCell>
                          <TableCell>
                            <span className="text-gray-600">${bid.maxBid.toLocaleString()}</span>
                          </TableCell>
                          <TableCell>
                            <div className="text-sm">
                              <div>{bid.bidTime.split(" ")[0]}</div>
                              <div className="text-gray-500">{bid.bidTime.split(" ")[1]}</div>
                            </div>
                          </TableCell>
                          <TableCell>{getStatusBadge(bid.status)}</TableCell>
                          <TableCell>
                            <Button size="sm" variant="outline" onClick={() => handleViewBid(bid)}>
                              <Eye className="w-4 h-4 mr-1" />
                              View
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              )}

              {/* Payment History Tab */}
              {activeTab === "payment" && (
                <div>
                  <h3 className="text-lg font-bold mb-4">Payment History</h3>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>PROPERTY</TableHead>
                        <TableHead>AMOUNT</TableHead>
                        <TableHead>DATE</TableHead>
                        <TableHead>METHOD</TableHead>
                        <TableHead>TRANSACTION ID</TableHead>
                        <TableHead>STATUS</TableHead>
                        <TableHead>ACTIONS</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {paymentHistory.map((payment) => (
                        <TableRow key={payment.id}>
                          <TableCell>
                            <div className="font-medium">{payment.property}</div>
                            <div className="text-sm text-gray-500">ID: {payment.id}</div>
                          </TableCell>
                          <TableCell>
                            <span className="font-medium">${payment.amount.toLocaleString()}</span>
                          </TableCell>
                          <TableCell>{payment.date}</TableCell>
                          <TableCell>{payment.method}</TableCell>
                          <TableCell>
                            <span className="font-mono text-sm">{payment.transactionId}</span>
                          </TableCell>
                          <TableCell>{getStatusBadge(payment.status)}</TableCell>
                          <TableCell>
                            <div className="flex items-center gap-2">
                              <Button size="sm" variant="outline" onClick={() => handleViewPayment(payment)}>
                                <Eye className="w-4 h-4" />
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => handleDownloadReport("payment", payment.id)}
                              >
                                <Download className="w-4 h-4" />
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              )}

              {/* Activity Log Tab */}
              {activeTab === "activity" && (
                <div>
                  <h3 className="text-lg font-bold mb-4">Activity Log</h3>
                  <div className="space-y-4">
                    {activityLog.map((activity) => (
                      <div key={activity.id} className="flex items-start gap-3 p-4 border rounded-lg">
                        {getActivityIcon(activity.type)}
                        <div className="flex-1">
                          <div className="flex items-center justify-between">
                            <div className="font-medium">{activity.action}</div>
                            <div className="text-sm text-gray-500">{activity.timestamp}</div>
                          </div>
                          <div className="text-sm text-gray-600 mt-1">{activity.description}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </Card>
        </div>
      </div>

      {/* View Property Modal */}
      <Dialog open={viewPropertyModal.open} onOpenChange={(open) => setViewPropertyModal({ open, property: null })}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Property Details</DialogTitle>
            <DialogDescription>Detailed information about the property listing.</DialogDescription>
          </DialogHeader>
          {viewPropertyModal.property && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label className="text-sm font-medium">Property Name</Label>
                  <p className="text-sm">{viewPropertyModal.property.name}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Category</Label>
                  <p className="text-sm">{viewPropertyModal.property.category}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Starting Price</Label>
                  <p className="text-sm">${viewPropertyModal.property.startingPrice.toLocaleString()}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Final Price</Label>
                  <p className="text-sm">
                    {viewPropertyModal.property.finalPrice
                      ? `$${viewPropertyModal.property.finalPrice.toLocaleString()}`
                      : "N/A"}
                  </p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Status</Label>
                  <div className="mt-1">{getStatusBadge(viewPropertyModal.property.status)}</div>
                </div>
                <div>
                  <Label className="text-sm font-medium">Performance</Label>
                  <p className="text-sm">
                    {viewPropertyModal.property.views} views, {viewPropertyModal.property.bids} bids
                  </p>
                </div>
              </div>
            </div>
          )}
          <DialogFooter>
            <Button variant="outline" onClick={() => setViewPropertyModal({ open: false, property: null })}>
              Close
            </Button>
            <Button onClick={() => router.push(`/products/${viewPropertyModal.property?.id}`)}>
              View Full Details
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* View Bid Modal */}
      <Dialog open={viewBidModal.open} onOpenChange={(open) => setViewBidModal({ open, bid: null })}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Bid Details</DialogTitle>
            <DialogDescription>Detailed information about this bid.</DialogDescription>
          </DialogHeader>
          {viewBidModal.bid && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label className="text-sm font-medium">Property</Label>
                  <p className="text-sm">{viewBidModal.bid.property}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Bid Amount</Label>
                  <p className="text-sm font-bold">${viewBidModal.bid.bidAmount.toLocaleString()}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Max Bid</Label>
                  <p className="text-sm">${viewBidModal.bid.maxBid.toLocaleString()}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Bid Time</Label>
                  <p className="text-sm">{viewBidModal.bid.bidTime}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Status</Label>
                  <div className="mt-1">{getStatusBadge(viewBidModal.bid.status)}</div>
                </div>
                <div>
                  <Label className="text-sm font-medium">Bid ID</Label>
                  <p className="text-sm font-mono">{viewBidModal.bid.id}</p>
                </div>
              </div>
            </div>
          )}
          <DialogFooter>
            <Button variant="outline" onClick={() => setViewBidModal({ open: false, bid: null })}>
              Close
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* View Payment Modal */}
      <Dialog open={viewPaymentModal.open} onOpenChange={(open) => setViewPaymentModal({ open, payment: null })}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Payment Details</DialogTitle>
            <DialogDescription>Detailed information about this payment transaction.</DialogDescription>
          </DialogHeader>
          {viewPaymentModal.payment && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label className="text-sm font-medium">Property</Label>
                  <p className="text-sm">{viewPaymentModal.payment.property}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Amount</Label>
                  <p className="text-sm font-bold">${viewPaymentModal.payment.amount.toLocaleString()}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Date</Label>
                  <p className="text-sm">{viewPaymentModal.payment.date}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Payment Method</Label>
                  <p className="text-sm">{viewPaymentModal.payment.method}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Transaction ID</Label>
                  <p className="text-sm font-mono">{viewPaymentModal.payment.transactionId}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Status</Label>
                  <div className="mt-1">{getStatusBadge(viewPaymentModal.payment.status)}</div>
                </div>
              </div>
            </div>
          )}
          <DialogFooter>
            <Button variant="outline" onClick={() => setViewPaymentModal({ open: false, payment: null })}>
              Close
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Send Message Modal */}
      <Dialog open={messageModal} onOpenChange={setMessageModal}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Send Message to Christina Brooks</DialogTitle>
            <DialogDescription>Send a direct message to the customer.</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="message">Message</Label>
              <Textarea
                id="message"
                placeholder="Type your message here..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                rows={4}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setMessageModal(false)}>
              Cancel
            </Button>
            <Button onClick={handleSendMessage}>Send Message</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit Profile Modal */}
      <Dialog open={editModal} onOpenChange={setEditModal}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Customer Profile</DialogTitle>
            <DialogDescription>Update customer information.</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="name">Full Name</Label>
              <Input
                id="name"
                value={editForm.name}
                onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
              />
            </div>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={editForm.email}
                onChange={(e) => setEditForm({ ...editForm, email: e.target.value })}
              />
            </div>
            <div>
              <Label htmlFor="phone">Phone</Label>
              <Input
                id="phone"
                value={editForm.phone}
                onChange={(e) => setEditForm({ ...editForm, phone: e.target.value })}
              />
            </div>
            <div>
              <Label htmlFor="address">Address</Label>
              <Textarea
                id="address"
                value={editForm.address}
                onChange={(e) => setEditForm({ ...editForm, address: e.target.value })}
                rows={3}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setEditModal(false)}>
              Cancel
            </Button>
            <Button onClick={handleEditProfile}>Save Changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Suspend Account Modal */}
      <Dialog open={suspendModal} onOpenChange={setSuspendModal}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-red-500" />
              Suspend Account
            </DialogTitle>
            <DialogDescription>
              Are you sure you want to suspend Christina Brooks' account? This action can be reversed later.
            </DialogDescription>
          </DialogHeader>
          <div className="p-4 bg-red-50 rounded-lg">
            <div className="text-sm text-red-700">
              <div className="font-medium">Warning:</div>
              <div>
                Suspending this account will prevent the user from accessing the platform and participating in auctions.
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setSuspendModal(false)}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleSuspend}>
              Suspend Account
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
