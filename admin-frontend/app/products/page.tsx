"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DollarSign,
  Users,
  TrendingUp,
  Search,
  Filter,
  Bell,
  Eye,
  Check,
  X,
  FolderPlus,
  Gavel,
  Clock,
} from "lucide-react"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Checkbox } from "@/components/ui/checkbox"
import Link from "next/link"
import { useToast } from "@/hooks/use-toast"
import { ApproveModal } from "@/components/modals/approve-modal"
import { RejectModal } from "@/components/modals/reject-modal"
import { AddToCatalogModal } from "@/components/modals/add-to-catalog-modal"

const pendingProducts = [
  {
    id: "00001",
    name: "Luxury Villa Santorini",
    address: "089 Kutch Green Apt. 448",
    owner: "Christina Brooks",
    submitted: "14 Feb 2019",
    status: "Pending",
    autoApproved: true,
  },
]

const activeAuctions = [
  {
    id: "00002",
    name: "Beachfront Villa Malibu",
    address: "123 Pacific Coast Highway",
    owner: "Michael Johnson",
    currentBid: "$12,500",
    bids: 28,
    timeLeft: "2h 15m",
    started: "15 Feb 2019",
  },
  {
    id: "00003",
    name: "Mountain Cabin Aspen",
    address: "456 Alpine Drive",
    owner: "Sarah Wilson",
    currentBid: "$8,900",
    bids: 15,
    timeLeft: "5h 30m",
    started: "14 Feb 2019",
  },
]

const completedAuctions = [
  {
    id: "00004",
    name: "Tokyo Penthouse",
    address: "789 Shibuya District",
    owner: "David Chen",
    finalBid: "$15,000",
    winner: "Christina Brooks",
    bids: 42,
    completed: "13 Feb 2019",
  },
  {
    id: "00005",
    name: "Paris Apartment",
    address: "321 Champs-Élysées",
    owner: "Emma Thompson",
    finalBid: "$9,200",
    winner: "Robert Kim",
    bids: 23,
    completed: "12 Feb 2019",
  },
]

export default function Products() {
  const [activeTab, setActiveTab] = useState("pending")
  const { toast } = useToast()

  const [approveModal, setApproveModal] = useState({ open: false, productId: "", productName: "" })
  const [rejectModal, setRejectModal] = useState({ open: false, productId: "", productName: "" })
  const [catalogModal, setCatalogModal] = useState({ open: false, productId: "", productName: "" })

  const handleApprove = (productId: string, productName: string) => {
    setApproveModal({ open: true, productId, productName })
  }

  const handleReject = (productId: string, productName: string) => {
    setRejectModal({ open: true, productId, productName })
  }

  const handleAddToCatalog = (productId: string, productName: string) => {
    setCatalogModal({ open: true, productId, productName })
  }

  const onApproveConfirm = (note?: string) => {
    toast({
      title: "Product Approved",
      description: `Product ${approveModal.productId} has been approved successfully.`,
    })
  }

  const onRejectConfirm = (reason: string, note?: string) => {
    toast({
      title: "Product Rejected",
      description: `Product ${rejectModal.productId} has been rejected. Reason: ${reason}`,
      variant: "destructive",
    })
  }

  const onCatalogConfirm = (category: string, featured: boolean) => {
    toast({
      title: "Added to Catalog",
      description: `Product ${catalogModal.productId} has been added to ${category} catalog${featured ? " as featured" : ""}.`,
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Products</h1>
          <div className="text-sm text-gray-500">Home &gt; Products</div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Active Bids</CardTitle>
            <DollarSign className="w-5 h-5 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Online Users</CardTitle>
            <Users className="w-5 h-5 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Revenue</CardTitle>
            <TrendingUp className="w-5 h-5 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">$0</div>
          </CardContent>
        </Card>
      </div>

      {/* Live Updates */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="w-5 h-5" />
            Live Updates
          </CardTitle>
        </CardHeader>
      </Card>

      {/* Filters */}
      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input placeholder="Search..." className="pl-10" />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4" />
          <span className="text-sm">Filter By</span>
        </div>
        <Select defaultValue="date">
          <SelectTrigger className="w-32">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="date">Date</SelectItem>
            <SelectItem value="name">Name</SelectItem>
            <SelectItem value="price">Price</SelectItem>
          </SelectContent>
        </Select>
        <Select defaultValue="status">
          <SelectTrigger className="w-32">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="status">Status</SelectItem>
            <SelectItem value="pending">Pending</SelectItem>
            <SelectItem value="approved">Approved</SelectItem>
          </SelectContent>
        </Select>
        <Select defaultValue="catalog">
          <SelectTrigger className="w-32">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="catalog">Catalog</SelectItem>
            <SelectItem value="residential">Residential</SelectItem>
            <SelectItem value="commercial">Commercial</SelectItem>
          </SelectContent>
        </Select>
        <Button variant="destructive">Reset Filter</Button>
      </div>

      {/* Tabs */}
      <div className="flex space-x-8 border-b">
        <button
          className={`pb-2 ${activeTab === "pending" ? "border-b-2 border-blue-500 text-blue-600 font-medium" : "text-gray-500 hover:text-gray-700"}`}
          onClick={() => setActiveTab("pending")}
        >
          Pending Approval (3)
        </button>
        <button
          className={`pb-2 ${activeTab === "active" ? "border-b-2 border-blue-500 text-blue-600 font-medium" : "text-gray-500 hover:text-gray-700"}`}
          onClick={() => setActiveTab("active")}
        >
          Active Auctions (2)
        </button>
        <button
          className={`pb-2 ${activeTab === "completed" ? "border-b-2 border-blue-500 text-blue-600 font-medium" : "text-gray-500 hover:text-gray-700"}`}
          onClick={() => setActiveTab("completed")}
        >
          Completed (2)
        </button>
      </div>

      {/* Products Table */}
      <Card>
        {activeTab === "pending" && (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-12">
                  <Checkbox />
                </TableHead>
                <TableHead>ID</TableHead>
                <TableHead>PROPERTY</TableHead>
                <TableHead>STATUS</TableHead>
                <TableHead>IMAGES</TableHead>
                <TableHead>OWNER</TableHead>
                <TableHead>SUBMITTED</TableHead>
                <TableHead>ACTION</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {pendingProducts.map((product) => (
                <TableRow key={product.id}>
                  <TableCell>
                    <Checkbox />
                  </TableCell>
                  <TableCell className="font-medium">{product.id}</TableCell>
                  <TableCell>
                    <div>
                      <div className="font-medium">{product.name}</div>
                      <div className="text-sm text-gray-500">{product.address}</div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <Badge className="bg-yellow-100 text-yellow-800">{product.status}</Badge>
                      {product.autoApproved && <Badge className="bg-green-100 text-green-800">Auto-Approved</Badge>}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <div className="w-8 h-8 bg-gray-200 rounded flex items-center justify-center">
                        <span className="text-xs">📷</span>
                      </div>
                      <div className="w-8 h-8 bg-gray-200 rounded flex items-center justify-center">
                        <span className="text-xs">📷</span>
                      </div>
                      <div className="w-8 h-8 bg-gray-200 rounded flex items-center justify-center">
                        <span className="text-xs">📷</span>
                      </div>
                      <Avatar className="w-8 h-8">
                        <AvatarImage src="/placeholder-user.jpg" />
                        <AvatarFallback>+</AvatarFallback>
                      </Avatar>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="font-medium">{product.owner}</div>
                  </TableCell>
                  <TableCell>{product.submitted}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Button
                        size="sm"
                        className="bg-green-500 hover:bg-green-600"
                        onClick={() => handleApprove(product.id, product.name)}
                      >
                        <Check className="w-4 h-4 mr-1" />
                        Approve
                      </Button>
                      <Button size="sm" variant="destructive" onClick={() => handleReject(product.id, product.name)}>
                        <X className="w-4 h-4 mr-1" />
                        Reject
                      </Button>
                      <Link href={`/products/${product.id}`}>
                        <Button size="sm" variant="outline">
                          <Eye className="w-4 h-4" />
                        </Button>
                      </Link>
                      <Button
                        size="sm"
                        variant="outline"
                        className="bg-blue-500 text-white border-blue-500"
                        onClick={() => handleAddToCatalog(product.id, product.name)}
                      >
                        <FolderPlus className="w-4 h-4 mr-1" />
                        Add to Catalog
                        <Badge className="ml-1 bg-white text-blue-500">1</Badge>
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}

        {activeTab === "active" && (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-12">
                  <Checkbox />
                </TableHead>
                <TableHead>ID</TableHead>
                <TableHead>PROPERTY</TableHead>
                <TableHead>OWNER</TableHead>
                <TableHead>CURRENT BID</TableHead>
                <TableHead>BIDS</TableHead>
                <TableHead>TIME LEFT</TableHead>
                <TableHead>STARTED</TableHead>
                <TableHead>ACTION</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {activeAuctions.map((auction) => (
                <TableRow key={auction.id}>
                  <TableCell>
                    <Checkbox />
                  </TableCell>
                  <TableCell className="font-medium">{auction.id}</TableCell>
                  <TableCell>
                    <div>
                      <div className="font-medium">{auction.name}</div>
                      <div className="text-sm text-gray-500">{auction.address}</div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="font-medium">{auction.owner}</div>
                  </TableCell>
                  <TableCell>
                    <div className="font-bold text-green-600">{auction.currentBid}</div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">{auction.bids}</Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4 text-orange-500" />
                      <span className="text-orange-600 font-medium">{auction.timeLeft}</span>
                    </div>
                  </TableCell>
                  <TableCell>{auction.started}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Link href={`/products/${auction.id}`}>
                        <Button size="sm" variant="outline">
                          <Eye className="w-4 h-4 mr-1" />
                          View
                        </Button>
                      </Link>
                      <Link href={`/auctions/${auction.id}`}>
                        <Button size="sm" className="bg-blue-500 hover:bg-blue-600">
                          <Gavel className="w-4 h-4 mr-1" />
                          Auction
                        </Button>
                      </Link>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}

        {activeTab === "completed" && (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-12">
                  <Checkbox />
                </TableHead>
                <TableHead>ID</TableHead>
                <TableHead>PROPERTY</TableHead>
                <TableHead>OWNER</TableHead>
                <TableHead>FINAL BID</TableHead>
                <TableHead>WINNER</TableHead>
                <TableHead>TOTAL BIDS</TableHead>
                <TableHead>COMPLETED</TableHead>
                <TableHead>ACTION</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {completedAuctions.map((auction) => (
                <TableRow key={auction.id}>
                  <TableCell>
                    <Checkbox />
                  </TableCell>
                  <TableCell className="font-medium">{auction.id}</TableCell>
                  <TableCell>
                    <div>
                      <div className="font-medium">{auction.name}</div>
                      <div className="text-sm text-gray-500">{auction.address}</div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="font-medium">{auction.owner}</div>
                  </TableCell>
                  <TableCell>
                    <div className="font-bold text-green-600">{auction.finalBid}</div>
                  </TableCell>
                  <TableCell>
                    <div className="font-medium text-blue-600">{auction.winner}</div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary">{auction.bids}</Badge>
                  </TableCell>
                  <TableCell>{auction.completed}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Link href={`/products/${auction.id}`}>
                        <Button size="sm" variant="outline">
                          <Eye className="w-4 h-4 mr-1" />
                          View
                        </Button>
                      </Link>
                      <Link href={`/auctions/${auction.id}`}>
                        <Button size="sm" variant="outline">
                          <Gavel className="w-4 h-4 mr-1" />
                          Details
                        </Button>
                      </Link>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </Card>
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
