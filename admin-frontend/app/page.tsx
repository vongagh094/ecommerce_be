import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  Users,
  ShoppingCart,
  DollarSign,
  Gavel,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Package,
  Calendar,
  CreditCard,
  Star,
  MapPin,
  Clock,
  Award,
} from "lucide-react"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  AreaChart,
  Area,
} from "recharts"

const salesData = [
  { name: "Jan", sales: 65000, bookings: 120, transactions: 85 },
  { name: "Feb", sales: 59000, bookings: 98, transactions: 72 },
  { name: "Mar", sales: 80000, bookings: 150, transactions: 110 },
  { name: "Apr", sales: 81000, bookings: 165, transactions: 125 },
  { name: "May", sales: 89000, bookings: 180, transactions: 140 },
  { name: "Jun", sales: 95000, bookings: 195, transactions: 155 },
]

const revenueData = [
  { period: "Today", amount: 2500 },
  { period: "This Week", amount: 18500 },
  { period: "This Month", amount: 95000 },
  { period: "This Quarter", amount: 285000 },
  { period: "This Year", amount: 1200000 },
]

const categoryData = [
  { name: "Luxury Villas", value: 45, color: "#3B82F6", count: 28 },
  { name: "Beach Houses", value: 30, color: "#10B981", count: 18 },
  { name: "City Apartments", value: 15, color: "#F59E0B", count: 12 },
  { name: "Mountain Cabins", value: 10, color: "#EF4444", count: 8 },
]

const userActivityData = [
  { time: "00:00", active: 120 },
  { time: "04:00", active: 80 },
  { time: "08:00", active: 350 },
  { time: "12:00", active: 450 },
  { time: "16:00", active: 380 },
  { time: "20:00", active: 280 },
  { time: "24:00", active: 150 },
]

const topProperties = [
  { name: "Santorini Villa", location: "Greece", rating: 4.9, bookings: 156, revenue: 45000 },
  { name: "Malibu Beach House", location: "California", rating: 4.8, bookings: 142, revenue: 38000 },
  { name: "Tokyo Penthouse", location: "Japan", rating: 4.7, bookings: 128, revenue: 52000 },
]

const recentAuctions = [
  { name: "Santorini Villa", currentBid: 12500, bids: 28, timeLeft: "2h 15m", status: "active" },
  { name: "Malibu Beach House", currentBid: 8900, bids: 15, timeLeft: "5h 30m", status: "active" },
  { name: "Tokyo Penthouse", currentBid: 15000, bids: 42, timeLeft: "Ended", status: "completed" },
]

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      {/* Main Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="relative overflow-hidden">
          <div className="absolute top-0 right-0 w-20 h-20 bg-purple-100 rounded-full -mr-10 -mt-10"></div>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Total Users</CardTitle>
            <Users className="w-5 h-5 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">40,689</div>
            <div className="flex items-center text-sm text-green-600">
              <TrendingUp className="w-4 h-4 mr-1" />
              8.5% Up from yesterday
            </div>
          </CardContent>
        </Card>

        <Card className="relative overflow-hidden">
          <div className="absolute top-0 right-0 w-20 h-20 bg-orange-100 rounded-full -mr-10 -mt-10"></div>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Total Orders</CardTitle>
            <ShoppingCart className="w-5 h-5 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">10,293</div>
            <div className="flex items-center text-sm text-green-600">
              <TrendingUp className="w-4 h-4 mr-1" />
              1.3% Up from past week
            </div>
          </CardContent>
        </Card>

        <Card className="relative overflow-hidden">
          <div className="absolute top-0 right-0 w-20 h-20 bg-green-100 rounded-full -mr-10 -mt-10"></div>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Total Sales</CardTitle>
            <DollarSign className="w-5 h-5 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$89,000</div>
            <div className="flex items-center text-sm text-red-600">
              <TrendingDown className="w-4 h-4 mr-1" />
              4.3% Down from yesterday
            </div>
          </CardContent>
        </Card>

        <Card className="relative overflow-hidden">
          <div className="absolute top-0 right-0 w-20 h-20 bg-blue-100 rounded-full -mr-10 -mt-10"></div>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Active Auctions</CardTitle>
            <Gavel className="w-5 h-5 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">156</div>
            <div className="flex items-center text-sm text-green-600">
              <TrendingUp className="w-4 h-4 mr-1" />
              12 new today
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Additional Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="bg-gradient-to-br from-indigo-50 to-indigo-100 border-indigo-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-indigo-700">Total Products</CardTitle>
            <Package className="w-5 h-5 text-indigo-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-indigo-900">1,245</div>
            <div className="flex items-center text-sm text-indigo-600">
              <TrendingUp className="w-4 h-4 mr-1" />
              25 added this week
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-cyan-50 to-cyan-100 border-cyan-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-cyan-700">Transactions Today</CardTitle>
            <CreditCard className="w-5 h-5 text-cyan-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-cyan-900">155</div>
            <div className="flex items-center text-sm text-cyan-600">
              <TrendingUp className="w-4 h-4 mr-1" />
              +18% from yesterday
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-yellow-50 to-yellow-100 border-yellow-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-yellow-700">Average Rating</CardTitle>
            <Star className="w-5 h-5 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-900">4.8</div>
            <div className="flex items-center text-sm text-yellow-600">
              <TrendingUp className="w-4 h-4 mr-1" />
              +0.2 from last month
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-pink-50 to-pink-100 border-pink-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-pink-700">Monthly Revenue</CardTitle>
            <Calendar className="w-5 h-5 text-pink-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-pink-900">$95,000</div>
            <div className="flex items-center text-sm text-pink-600">
              <TrendingUp className="w-4 h-4 mr-1" />
              +12% from last month
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Sales & Transactions Chart */}
        <Card className="lg:col-span-2 relative overflow-hidden">
          <div
            className="absolute inset-0 opacity-5"
            style={{
              backgroundImage: "url('/images/analytics-bg.png')",
              backgroundSize: "cover",
              backgroundPosition: "center",
            }}
          />
          <CardHeader className="relative z-10">
            <CardTitle>Sales & Transactions Overview</CardTitle>
          </CardHeader>
          <CardContent className="relative z-10">
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={salesData}>
                <defs>
                  <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorBookings" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Area
                  type="monotone"
                  dataKey="sales"
                  stroke="#3B82F6"
                  fillOpacity={1}
                  fill="url(#colorSales)"
                  name="Sales ($)"
                />
                <Area
                  type="monotone"
                  dataKey="bookings"
                  stroke="#10B981"
                  fillOpacity={1}
                  fill="url(#colorBookings)"
                  name="Bookings"
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Top Properties */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Award className="w-5 h-5 text-yellow-500" />
              Top Properties
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {topProperties.map((property, index) => (
              <div key={index} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-purple-500 rounded-lg flex items-center justify-center text-white font-bold">
                  #{index + 1}
                </div>
                <div className="flex-1">
                  <div className="font-medium">{property.name}</div>
                  <div className="text-sm text-gray-500 flex items-center gap-1">
                    <MapPin className="w-3 h-3" />
                    {property.location}
                  </div>
                  <div className="flex items-center gap-2 mt-1">
                    <div className="flex items-center gap-1">
                      <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
                      <span className="text-xs">{property.rating}</span>
                    </div>
                    <span className="text-xs text-gray-500">•</span>
                    <span className="text-xs text-gray-500">{property.bookings} bookings</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-green-600">${property.revenue.toLocaleString()}</div>
                  <div className="text-xs text-gray-500">revenue</div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* User Activity Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="w-5 h-5 text-blue-500" />
              User Activity (24h)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={userActivityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="active"
                  stroke="#3B82F6"
                  strokeWidth={3}
                  dot={{ fill: "#3B82F6", strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Revenue by Period */}
        <Card>
          <CardHeader>
            <CardTitle>Revenue by Period</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={revenueData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="period" />
                <YAxis />
                <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, "Revenue"]} />
                <Bar dataKey="amount" fill="#3B82F6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Property Categories Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Property Categories</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value, name, props) => [`${props.payload.count} properties`, name]} />
              </PieChart>
            </ResponsiveContainer>
            <div className="grid grid-cols-1 gap-2 mt-4">
              {categoryData.map((item, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                    <span className="text-sm">{item.name}</span>
                  </div>
                  <span className="text-xs text-gray-500 font-medium">{item.count}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Reports */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            Recent Reports
          </CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="space-y-2">
            <div className="flex items-start gap-3 p-4 bg-red-50 rounded-lg border border-red-200">
              <div className="w-2 h-2 bg-red-500 rounded-full mt-2"></div>
              <div className="flex-1">
                <div className="font-medium">Luxury Villa Santorini</div>
                <div className="text-sm text-gray-500">Inappropriate Content</div>
                <div className="flex items-center justify-between mt-2">
                  <Badge variant="destructive" className="text-xs">
                    High
                  </Badge>
                  <span className="text-xs text-gray-400">2 hours ago</span>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-start gap-3 p-4 bg-red-50 rounded-lg border border-red-200">
              <div className="w-2 h-2 bg-red-500 rounded-full mt-2"></div>
              <div className="flex-1">
                <div className="font-medium">Beach House Malibu</div>
                <div className="text-sm text-gray-500">Fake Property</div>
                <div className="flex items-center justify-between mt-2">
                  <Badge variant="destructive" className="text-xs">
                    Critical
                  </Badge>
                  <span className="text-xs text-gray-400">4 hours ago</span>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-start gap-3 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
              <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2"></div>
              <div className="flex-1">
                <div className="font-medium">Mountain Cabin Aspen</div>
                <div className="text-sm text-gray-500">Misleading Info</div>
                <div className="flex items-center justify-between mt-2">
                  <Badge variant="secondary" className="text-xs">
                    Medium
                  </Badge>
                  <span className="text-xs text-gray-400">6 hours ago</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recent Auctions with Property Showcase */}
      <Card className="relative overflow-hidden">
        <div
          className="absolute top-0 right-0 w-64 h-32 opacity-10"
          style={{
            backgroundImage: "url('/images/property-showcase.png')",
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        />
        <CardHeader className="relative z-10">
          <CardTitle>Recent Auctions</CardTitle>
        </CardHeader>
        <CardContent className="relative z-10 space-y-4">
          {recentAuctions.map((auction, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg border"
            >
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-purple-500 rounded-lg flex items-center justify-center">
                  <Gavel className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                  <div className="font-medium">{auction.name}</div>
                  <div className="text-sm text-gray-500">{auction.bids} bids</div>
                </div>
              </div>
              <div className="text-right">
                <div className="font-bold text-green-600">${auction.currentBid.toLocaleString()}</div>
                <div className="text-sm text-gray-500">{auction.timeLeft}</div>
              </div>
              <Badge
                className={
                  auction.status === "active" ? "bg-green-100 text-green-800 ml-4" : "bg-gray-100 text-gray-800 ml-4"
                }
              >
                {auction.status}
              </Badge>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
