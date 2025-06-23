"use client"

import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { X, AlertTriangle } from "lucide-react"

interface RejectModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  productName: string
  onConfirm: (reason: string, note?: string) => void
}

const rejectReasons = [
  "Inappropriate Content",
  "Fake Property",
  "Misleading Information",
  "Poor Quality Images",
  "Incomplete Information",
  "Violation of Terms",
  "Other",
]

export function RejectModal({ open, onOpenChange, productName, onConfirm }: RejectModalProps) {
  const [reason, setReason] = useState("")
  const [note, setNote] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleConfirm = async () => {
    if (!reason) return

    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 1000)) // Simulate API call
    onConfirm(reason, note)
    setIsLoading(false)
    onOpenChange(false)
    setReason("")
    setNote("")
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
              <X className="w-4 h-4 text-red-600" />
            </div>
            Reject Product
          </DialogTitle>
          <DialogDescription>
            You are about to reject "{productName}". Please provide a reason for rejection.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="reason">Rejection Reason *</Label>
            <Select value={reason} onValueChange={setReason}>
              <SelectTrigger>
                <SelectValue placeholder="Select a reason" />
              </SelectTrigger>
              <SelectContent>
                {rejectReasons.map((r) => (
                  <SelectItem key={r} value={r}>
                    {r}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="note">Additional Notes</Label>
            <Textarea
              id="note"
              placeholder="Provide additional details about the rejection..."
              value={note}
              onChange={(e) => setNote(e.target.value)}
              rows={3}
            />
          </div>

          <div className="flex items-start gap-2 p-3 bg-red-50 rounded-lg">
            <AlertTriangle className="w-4 h-4 text-red-600 mt-0.5" />
            <div className="text-sm text-red-700">
              The property owner will be notified about this rejection and the reason provided.
            </div>
          </div>
        </div>

        <DialogFooter className="flex gap-2">
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={isLoading}>
            Cancel
          </Button>
          <Button onClick={handleConfirm} disabled={isLoading || !reason} variant="destructive">
            {isLoading ? "Rejecting..." : "Reject Product"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
