"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { useToast } from "@/hooks/use-toast"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Clock, AlertTriangle, CheckCircle, XCircle, Search, Eye, Trash2 } from "lucide-react"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

export default function Reports() {
  const [removeReportModal, setRemoveReportModal] = useState({ open: false, report: null as any })
  const { toast } = useToast()
  const router = useRouter()

  const handleViewReport = (reportId: string) => {
    router.push(`/reports/${reportId}`)
  }

  const handleRemoveReport = (report: any) => {
    setRemoveReportModal({ open: true, report })
  }

  const confirmRemoveReport = () => {
    if (removeReportModal.report) {
      toast({
        title: "Report Removed",
        description: `Report ${removeReportModal.report.id} has been removed and the product has been taken down.`,
        variant: "destructive",
      })
      setRemoveReportModal({ open: false, report: null })
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Reports</h1>
          <div className="text-sm text-gray-500">Home &gt; Reports</div>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input placeholder="Search reports..." className="pl-10" />
        </div>
        <Select defaultValue="all">
          <SelectTrigger className="w-40">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Categories</SelectItem>
            <SelectItem value="content">Content</SelectItem>
            <SelectItem value="fraud">Fraud</SelectItem>
          </SelectContent>
        </Select>
        <Select defaultValue="all">
          <SelectTrigger className="w-32">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Priority</SelectItem>
            <SelectItem value="high">High</SelectItem>
            <SelectItem value="critical">Critical</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Pending Reports</CardTitle>
            <Clock className="w-5 h-5 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Critical Reports</CardTitle>
            <AlertTriangle className="w-5 h-5 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Resolved Today</CardTitle>
            <CheckCircle className="w-5 h-5 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">5</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Products Removed</CardTitle>
            <XCircle className="w-5 h-5 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <div className="flex space-x-8 border-b">
        <button className="pb-2 border-b-2 border-blue-500 text-blue-600 font-medium">Pending Reports (3)</button>
        <button className="pb-2 text-gray-500 hover:text-gray-700">Reviewed Reports (2)</button>
      </div>

      {/* Reports Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-12">
                <Checkbox />
              </TableHead>
              <TableHead>REPORT ID</TableHead>
              <TableHead>PRODUCT</TableHead>
              <TableHead>REPORTED BY</TableHead>
              <TableHead>REASON</TableHead>
              <TableHead>PRIORITY</TableHead>
              <TableHead>DATE</TableHead>
              <TableHead>STATUS</TableHead>
              <TableHead>ACTION</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableCell>
                <Checkbox />
              </TableCell>
              <TableCell className="font-medium">RPT001</TableCell>
              <TableCell>
                <div>
                  <div className="font-medium">Luxury Villa Santorini</div>
                  <div className="text-sm text-gray-500">ID: 00001</div>
                </div>
              </TableCell>
              <TableCell>
                <div>
                  <div className="font-medium">John Smith</div>
                  <div className="text-sm text-gray-500">john@example.com</div>
                </div>
              </TableCell>
              <TableCell>
                <div>
                  <div className="font-medium">Inappropriate Content</div>
                  <div className="text-sm text-gray-500">Misleading Information</div>
                </div>
              </TableCell>
              <TableCell>
                <Badge variant="destructive">High</Badge>
              </TableCell>
              <TableCell>
                <div className="text-sm">
                  <div>2024-01-15</div>
                  <div className="text-gray-500">14:30</div>
                </div>
              </TableCell>
              <TableCell>
                <Badge className="bg-yellow-100 text-yellow-800">Pending</Badge>
              </TableCell>
              <TableCell>
                <div className="flex items-center gap-2">
                  <Button size="sm" variant="outline" onClick={() => handleViewReport("RPT001")}>
                    <Eye className="w-4 h-4" />
                    View
                  </Button>
                  <Button
                    size="sm"
                    variant="destructive"
                    onClick={() =>
                      handleRemoveReport({
                        id: "RPT001",
                        productName: "Luxury Villa Santorini",
                        productId: "00001",
                      })
                    }
                  >
                    <Trash2 className="w-4 h-4" />
                    Remove
                  </Button>
                </div>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>
                <Checkbox />
              </TableCell>
              <TableCell className="font-medium">RPT002</TableCell>
              <TableCell>
                <div>
                  <div className="font-medium">Beach House Malibu</div>
                  <div className="text-sm text-gray-500">ID: 00003</div>
                </div>
              </TableCell>
              <TableCell>
                <div>
                  <div className="font-medium">Sarah Johnson</div>
                  <div className="text-sm text-gray-500">sarah@example.com</div>
                </div>
              </TableCell>
              <TableCell>
                <div>
                  <div className="font-medium">Fake Property</div>
                  <div className="text-sm text-gray-500">Fraud</div>
                </div>
              </TableCell>
              <TableCell>
                <Badge variant="destructive">Critical</Badge>
              </TableCell>
              <TableCell>
                <div className="text-sm">
                  <div>2024-01-14</div>
                  <div className="text-gray-500">09:15</div>
                </div>
              </TableCell>
              <TableCell>
                <Badge className="bg-yellow-100 text-yellow-800">Pending</Badge>
              </TableCell>
              <TableCell>
                <div className="flex items-center gap-2">
                  <Button size="sm" variant="outline" onClick={() => handleViewReport("RPT002")}>
                    <Eye className="w-4 h-4" />
                    View
                  </Button>
                  <Button
                    size="sm"
                    variant="destructive"
                    onClick={() =>
                      handleRemoveReport({
                        id: "RPT002",
                        productName: "Beach House Malibu",
                        productId: "00003",
                      })
                    }
                  >
                    <Trash2 className="w-4 h-4" />
                    Remove
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </Card>

      {/* Remove Report Modal */}
      <Dialog open={removeReportModal.open} onOpenChange={(open) => setRemoveReportModal({ open, report: null })}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-red-500" />
              Remove Product
            </DialogTitle>
            <DialogDescription>
              Are you sure you want to remove this product? This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          {removeReportModal.report && (
            <div className="space-y-4">
              <div className="p-4 bg-red-50 rounded-lg">
                <div className="font-medium text-red-800">Product to be removed:</div>
                <div className="text-red-700">{removeReportModal.report.productName}</div>
                <div className="text-sm text-red-600">ID: {removeReportModal.report.productId}</div>
              </div>

              <div className="p-4 bg-yellow-50 rounded-lg">
                <div className="flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-600 mt-0.5" />
                  <div className="text-sm text-yellow-700">
                    <div className="font-medium">Warning:</div>
                    <div>Removing this product will:</div>
                    <ul className="list-disc list-inside mt-1 space-y-1">
                      <li>Immediately take down the property listing</li>
                      <li>Cancel any active auctions</li>
                      <li>Notify the property owner</li>
                      <li>Refund any pending bids</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}
          <DialogFooter>
            <Button variant="outline" onClick={() => setRemoveReportModal({ open: false, report: null })}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={confirmRemoveReport}>
              Remove Product
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
