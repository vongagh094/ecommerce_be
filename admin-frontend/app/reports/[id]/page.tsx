"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import {
  ArrowLeft,
  AlertTriangle,
  XCircle,
  Eye,
  MessageSquare,
  Clock,
  User,
  FileText,
  Calendar,
  Flag,
  Shield,
  Trash2,
  Send,
} from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import Link from "next/link"
import { useParams, useRouter } from "next/navigation"
import { useToast } from "@/hooks/use-toast"

// Mock data for the report
const reportData = {
  RPT001: {
    id: "RPT001",
    productName: "Luxury Villa Santorini",
    productId: "00001",
    reportedBy: "John Smith",
    reporterEmail: "john@example.com",
    reporterPhone: "+1 (555) 123-4567",
    reason: "Inappropriate Content",
    category: "Content Violation",
    description:
      "The property listing contains misleading information about amenities and location. The photos appear to be stock images and don't match the actual property.",
    priority: "High",
    date: "2024-01-15",
    time: "14:30",
    status: "Pending",
    evidence: [
      "Screenshot of misleading photos",
      "Comparison with actual property images",
      "Customer complaint emails",
    ],
    previousReports: 2,
    reporterHistory: "First time reporter",
  },
  RPT002: {
    id: "RPT002",
    productName: "Beach House Malibu",
    productId: "00003",
    reportedBy: "Sarah Johnson",
    reporterEmail: "sarah@example.com",
    reporterPhone: "+1 (555) 987-6543",
    reason: "Fake Property",
    category: "Fraud",
    description:
      "This property doesn't exist at the listed address. I visited the location and found a completely different building. This appears to be a scam listing.",
    priority: "Critical",
    date: "2024-01-14",
    time: "09:15",
    status: "Pending",
    evidence: ["Photos from actual location visit", "Google Street View comparison", "Property records verification"],
    previousReports: 0,
    reporterHistory: "Verified user with 15+ bookings",
  },
}

export default function ReportDetail() {
  const params = useParams()
  const router = useRouter()
  const { toast } = useToast()
  const [actionModal, setActionModal] = useState({ open: false, action: "" })
  const [contactModal, setContactModal] = useState(false)
  const [adminNote, setAdminNote] = useState("")
  const [contactForm, setContactForm] = useState({
    subject: "",
    message: "",
  })

  const reportId = params.id as string
  const report = reportData[reportId as keyof typeof reportData]

  if (!report) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Report Not Found</h2>
          <p className="text-gray-600 mt-2">The report you're looking for doesn't exist.</p>
          <Link href="/reports">
            <Button className="mt-4">Back to Reports</Button>
          </Link>
        </div>
      </div>
    )
  }

  const handleAction = (action: string) => {
    setActionModal({ open: true, action })
  }

  const handleContactReporter = () => {
    setContactModal(true)
  }

  const confirmAction = () => {
    const actionMessages = {
      reject: "Report has been rejected as invalid. The product remains active and the reporter has been notified.",
      "suspend-product": "Report has been approved. The product has been suspended pending further investigation.",
      "remove-product": "Report has been approved. The product has been permanently removed from the platform.",
    }

    const actionVariants = {
      reject: "default" as const,
      "suspend-product": "destructive" as const,
      "remove-product": "destructive" as const,
    }

    toast({
      title: "Action Completed",
      description: actionMessages[actionModal.action as keyof typeof actionMessages],
      variant: actionVariants[actionModal.action as keyof typeof actionVariants],
    })

    setActionModal({ open: false, action: "" })
    setAdminNote("")

    // Navigate back to reports after action
    setTimeout(() => {
      router.push("/reports")
    }, 2000)
  }

  const sendMessage = () => {
    if (!contactForm.subject.trim() || !contactForm.message.trim()) {
      toast({
        title: "Error",
        description: "Please fill in both subject and message fields.",
        variant: "destructive",
      })
      return
    }

    toast({
      title: "Message Sent",
      description: `Your message has been sent to ${report.reportedBy}.`,
    })

    setContactModal(false)
    setContactForm({ subject: "", message: "" })
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "Critical":
        return "bg-red-100 text-red-800"
      case "High":
        return "bg-orange-100 text-orange-800"
      case "Medium":
        return "bg-yellow-100 text-yellow-800"
      case "Low":
        return "bg-green-100 text-green-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Pending":
        return "bg-yellow-100 text-yellow-800"
      case "Resolved":
        return "bg-green-100 text-green-800"
      case "Rejected":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href="/reports">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-4 h-4" />
            </Button>
          </Link>
          <div>
            <h1 className="text-2xl font-bold">Report Details</h1>
            <div className="text-sm text-gray-500">Home &gt; Reports &gt; {report.id}</div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Badge className={getPriorityColor(report.priority)}>{report.priority} Priority</Badge>
          <Badge className={getStatusColor(report.status)}>{report.status}</Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Report Overview */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Flag className="w-5 h-5 text-red-500" />
                Report Overview
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label className="text-sm font-medium text-gray-600">Report ID</Label>
                  <p className="font-mono text-sm">{report.id}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium text-gray-600">Date Reported</Label>
                  <p className="text-sm">
                    {report.date} at {report.time}
                  </p>
                </div>
                <div>
                  <Label className="text-sm font-medium text-gray-600">Category</Label>
                  <p className="text-sm">{report.category}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium text-gray-600">Reason</Label>
                  <p className="text-sm">{report.reason}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Reported Product */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-blue-500" />
                Reported Product
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg">
                <div className="w-16 h-16 bg-gray-200 rounded-lg flex items-center justify-center">
                  <span className="text-2xl">🏠</span>
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-lg">{report.productName}</h3>
                  <p className="text-sm text-gray-600">Product ID: {report.productId}</p>
                  <div className="flex items-center gap-2 mt-2">
                    <Link href={`/products/${report.productId}`}>
                      <Button size="sm" variant="outline">
                        <Eye className="w-4 h-4 mr-2" />
                        View Product
                      </Button>
                    </Link>
                    <Badge variant="outline">{report.previousReports} previous reports</Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Report Details */}
          <Card>
            <CardHeader>
              <CardTitle>Report Description</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <Label className="text-sm font-medium text-gray-600">Detailed Description</Label>
                  <div className="mt-2 p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm leading-relaxed">{report.description}</p>
                  </div>
                </div>

                <div>
                  <Label className="text-sm font-medium text-gray-600">Evidence Provided</Label>
                  <div className="mt-2 space-y-2">
                    {report.evidence.map((item, index) => (
                      <div key={index} className="flex items-center gap-2 p-2 bg-blue-50 rounded">
                        <FileText className="w-4 h-4 text-blue-600" />
                        <span className="text-sm">{item}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Reporter Information */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="w-5 h-5 text-purple-500" />
                Reporter Information
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-start gap-4">
                <Avatar className="w-12 h-12">
                  <AvatarImage src="/placeholder-user.jpg" />
                  <AvatarFallback>
                    {report.reportedBy
                      .split(" ")
                      .map((n) => n[0])
                      .join("")}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <h3 className="font-semibold">{report.reportedBy}</h3>
                  <p className="text-sm text-gray-600">{report.reporterEmail}</p>
                  <p className="text-sm text-gray-600">{report.reporterPhone}</p>
                  <div className="mt-2">
                    <Badge variant="outline">{report.reporterHistory}</Badge>
                  </div>
                </div>
                <Button size="sm" variant="outline" onClick={handleContactReporter}>
                  <MessageSquare className="w-4 h-4 mr-2" />
                  Contact Reporter
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="w-5 h-5 text-green-500" />
                Quick Actions
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button
                variant="outline"
                className="w-full bg-red-50 text-red-700 border-red-200 hover:bg-red-100"
                onClick={() => handleAction("reject")}
              >
                <XCircle className="w-4 h-4 mr-2" />
                Reject Report
              </Button>
              <Button
                variant="outline"
                className="w-full bg-yellow-50 text-yellow-700 border-yellow-200 hover:bg-yellow-100"
                onClick={() => handleAction("suspend-product")}
              >
                <Clock className="w-4 h-4 mr-2" />
                Approve & Suspend Product
              </Button>
              <Button variant="destructive" className="w-full" onClick={() => handleAction("remove-product")}>
                <Trash2 className="w-4 h-4 mr-2" />
                Approve & Remove Product
              </Button>
            </CardContent>
          </Card>

          {/* Report Statistics */}
          <Card>
            <CardHeader>
              <CardTitle>Report Statistics</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Priority Level</span>
                <Badge className={getPriorityColor(report.priority)}>{report.priority}</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Previous Reports</span>
                <span className="font-medium">{report.previousReports}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Reporter Status</span>
                <Badge variant="outline">Verified</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Response Time</span>
                <span className="font-medium">{"< 24h"}</span>
              </div>
            </CardContent>
          </Card>

          {/* Timeline */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="w-5 h-5 text-blue-500" />
                Timeline
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-red-500 rounded-full mt-2"></div>
                  <div>
                    <div className="font-medium text-sm">Report Submitted</div>
                    <div className="text-xs text-gray-500">
                      {report.date} {report.time}
                    </div>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2"></div>
                  <div>
                    <div className="font-medium text-sm">Under Review</div>
                    <div className="text-xs text-gray-500">Current status</div>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-gray-300 rounded-full mt-2"></div>
                  <div>
                    <div className="font-medium text-sm text-gray-400">Pending Action</div>
                    <div className="text-xs text-gray-400">Awaiting admin decision</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Action Confirmation Modal */}
      <Dialog open={actionModal.open} onOpenChange={(open) => setActionModal({ open, action: "" })}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              {actionModal.action === "remove-product" && <Trash2 className="w-5 h-5 text-red-500" />}
              {actionModal.action === "reject" && <XCircle className="w-5 h-5 text-red-500" />}
              {actionModal.action === "suspend-product" && <Clock className="w-5 h-5 text-yellow-500" />}
              Confirm Action
            </DialogTitle>
            <DialogDescription>
              {actionModal.action === "reject" &&
                "Reject this report as invalid or unfounded. The product will remain active."}
              {actionModal.action === "remove-product" &&
                "Approve this report and permanently remove the product from the platform."}
              {actionModal.action === "suspend-product" &&
                "Approve this report and temporarily suspend the product pending investigation."}
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            <div>
              <Label htmlFor="adminNote">Admin Note (Optional)</Label>
              <Textarea
                id="adminNote"
                placeholder="Add any notes about this decision..."
                value={adminNote}
                onChange={(e) => setAdminNote(e.target.value)}
                rows={3}
              />
            </div>

            {(actionModal.action === "remove-product" || actionModal.action === "suspend-product") && (
              <div className="p-3 bg-red-50 rounded-lg">
                <div className="flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-red-600 mt-0.5" />
                  <div className="text-sm text-red-700">
                    <div className="font-medium">Warning:</div>
                    <div>This action will affect the product owner and any active auctions.</div>
                  </div>
                </div>
              </div>
            )}
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setActionModal({ open: false, action: "" })}>
              Cancel
            </Button>
            <Button
              onClick={confirmAction}
              variant={
                actionModal.action === "remove-product" || actionModal.action === "suspend-product"
                  ? "destructive"
                  : "default"
              }
            >
              Confirm{" "}
              {actionModal.action === "reject"
                ? "Rejection"
                : actionModal.action === "suspend-product"
                  ? "Suspension"
                  : "Removal"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Contact Reporter Modal */}
      <Dialog open={contactModal} onOpenChange={setContactModal}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <MessageSquare className="w-5 h-5 text-blue-500" />
              Contact Reporter
            </DialogTitle>
            <DialogDescription>Send a message to {report.reportedBy} regarding their report.</DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            <div className="p-3 bg-blue-50 rounded-lg">
              <div className="text-sm text-blue-700">
                <div className="font-medium">Reporter: {report.reportedBy}</div>
                <div>Email: {report.reporterEmail}</div>
                <div>Report ID: {report.id}</div>
              </div>
            </div>

            <div>
              <Label htmlFor="subject">Subject</Label>
              <Input
                id="subject"
                placeholder="Enter message subject..."
                value={contactForm.subject}
                onChange={(e) => setContactForm({ ...contactForm, subject: e.target.value })}
              />
            </div>

            <div>
              <Label htmlFor="message">Message</Label>
              <Textarea
                id="message"
                placeholder="Type your message here..."
                value={contactForm.message}
                onChange={(e) => setContactForm({ ...contactForm, message: e.target.value })}
                rows={4}
              />
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setContactModal(false)}>
              Cancel
            </Button>
            <Button onClick={sendMessage}>
              <Send className="w-4 h-4 mr-2" />
              Send Message
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
