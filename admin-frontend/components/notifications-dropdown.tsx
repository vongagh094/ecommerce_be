"use client"

import { useState } from "react"
import { Bell, Check, X, AlertTriangle, Info, CheckCircle, Clock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { DropdownMenu, DropdownMenuContent, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { useToast } from "@/hooks/use-toast"

interface Notification {
  id: string
  type: "info" | "warning" | "success" | "error"
  title: string
  message: string
  time: string
  isRead: boolean
  actionRequired?: boolean
}

const mockNotifications: Notification[] = [
  {
    id: "1",
    type: "warning",
    title: "New Report Submitted",
    message: "A new report has been submitted for Luxury Villa Santorini regarding inappropriate content.",
    time: "2 minutes ago",
    isRead: false,
    actionRequired: true,
  },
  {
    id: "2",
    type: "success",
    title: "Auction Completed",
    message: "Tokyo Penthouse auction has ended successfully with a winning bid of $15,000.",
    time: "15 minutes ago",
    isRead: false,
  },
  {
    id: "3",
    type: "info",
    title: "New User Registration",
    message: "5 new users have registered in the last hour.",
    time: "1 hour ago",
    isRead: false,
  },
  {
    id: "4",
    type: "error",
    title: "Payment Failed",
    message: "Payment processing failed for order #12345. Customer has been notified.",
    time: "2 hours ago",
    isRead: true,
  },
  {
    id: "5",
    type: "success",
    title: "Product Approved",
    message: "Mountain Cabin Aspen has been approved and is now live on the platform.",
    time: "3 hours ago",
    isRead: true,
  },
  {
    id: "6",
    type: "warning",
    title: "High Traffic Alert",
    message: "Website traffic is 150% above normal. Monitor server performance.",
    time: "4 hours ago",
    isRead: true,
  },
]

export function NotificationsDropdown() {
  const [notifications, setNotifications] = useState<Notification[]>(mockNotifications)
  const { toast } = useToast()

  const unreadCount = notifications.filter((n) => !n.isRead).length

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case "warning":
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />
      case "error":
        return <X className="w-4 h-4 text-red-500" />
      case "success":
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case "info":
      default:
        return <Info className="w-4 h-4 text-blue-500" />
    }
  }

  const getNotificationBg = (type: string, isRead: boolean) => {
    if (isRead) return "bg-gray-50"

    switch (type) {
      case "warning":
        return "bg-yellow-50 border-yellow-200"
      case "error":
        return "bg-red-50 border-red-200"
      case "success":
        return "bg-green-50 border-green-200"
      case "info":
      default:
        return "bg-blue-50 border-blue-200"
    }
  }

  const markAsRead = (id: string) => {
    setNotifications((prev) =>
      prev.map((notification) => (notification.id === id ? { ...notification, isRead: true } : notification)),
    )
  }

  const markAllAsRead = () => {
    setNotifications((prev) => prev.map((notification) => ({ ...notification, isRead: true })))
    toast({
      title: "All notifications marked as read",
      description: "All notifications have been marked as read.",
    })
  }

  const deleteNotification = (id: string) => {
    setNotifications((prev) => prev.filter((notification) => notification.id !== id))
    toast({
      title: "Notification deleted",
      description: "The notification has been removed.",
    })
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="w-5 h-5" />
          {unreadCount > 0 && (
            <Badge className="absolute -top-1 -right-1 w-5 h-5 p-0 flex items-center justify-center bg-red-500 text-xs">
              {unreadCount > 9 ? "9+" : unreadCount}
            </Badge>
          )}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-96 p-0">
        <div className="p-4 border-b">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold">Notifications</h3>
            {unreadCount > 0 && (
              <Button variant="ghost" size="sm" onClick={markAllAsRead}>
                Mark all as read
              </Button>
            )}
          </div>
          {unreadCount > 0 && <p className="text-sm text-gray-500 mt-1">{unreadCount} unread notifications</p>}
        </div>

        <ScrollArea className="h-96">
          <div className="p-2">
            {notifications.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <Bell className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>No notifications</p>
              </div>
            ) : (
              <div className="space-y-2">
                {notifications.map((notification) => (
                  <div
                    key={notification.id}
                    className={`p-3 rounded-lg border transition-colors ${getNotificationBg(
                      notification.type,
                      notification.isRead,
                    )} ${!notification.isRead ? "border" : ""}`}
                  >
                    <div className="flex items-start gap-3">
                      <div className="mt-0.5">{getNotificationIcon(notification.type)}</div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between gap-2">
                          <div className="flex-1">
                            <h4
                              className={`text-sm font-medium ${!notification.isRead ? "text-gray-900" : "text-gray-600"}`}
                            >
                              {notification.title}
                              {notification.actionRequired && (
                                <Badge variant="destructive" className="ml-2 text-xs">
                                  Action Required
                                </Badge>
                              )}
                            </h4>
                            <p className="text-xs text-gray-500 mt-1 line-clamp-2">{notification.message}</p>
                            <div className="flex items-center gap-2 mt-2">
                              <div className="flex items-center gap-1 text-xs text-gray-400">
                                <Clock className="w-3 h-3" />
                                {notification.time}
                              </div>
                              {!notification.isRead && <div className="w-2 h-2 bg-blue-500 rounded-full"></div>}
                            </div>
                          </div>
                          <div className="flex items-center gap-1">
                            {!notification.isRead && (
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => markAsRead(notification.id)}
                                className="h-6 w-6 p-0"
                              >
                                <Check className="w-3 h-3" />
                              </Button>
                            )}
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => deleteNotification(notification.id)}
                              className="h-6 w-6 p-0 text-gray-400 hover:text-red-500"
                            >
                              <X className="w-3 h-3" />
                            </Button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </ScrollArea>

        <div className="p-3 border-t">
          <Button variant="outline" className="w-full" size="sm">
            View All Notifications
          </Button>
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
