import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Plus, Search, Eye } from "lucide-react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import Link from "next/link"

export default function Customers() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Customers</h1>
          <div className="text-sm text-gray-500">Home &gt; Customers</div>
        </div>
        text-gray-400 w-4 h-4" />
        <Input placeholder="Search >
      </di<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-plus w-4 h-4 mr-2" __v0_r="0,786,800"><path d="M5 12h14"></path><path d="M12 5v14"></path></svg>Add Customeriv className="bg-white rounded-lg border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>NAME</TableHead>
              <TableHead>ADDRESS</TableHead>
              <TableHead>DATE</TableHead>
              <TableHead>SPENT</TableHead>
              <TableHead>WINS</TableHead>
              <TableHead>STATUS</TableHead>
              <TableHead>ACTION</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableCell className="font-medium">00001</TableCell>
              <TableCell>
                <div className="flex items-center gap-3">
                  <Avatar className="w-8 h-8">
                    <AvatarImage src="/placeholder-user.jpg" />
                    <AvatarFallback>CB</AvatarFallback>
                  </Avatar>
                  <span className="font-medium">Christina Brooks</span>
                </div>
              </TableCell>
              <TableCell className="text-gray-500">089 Kutch Green Apt. 448</TableCell>
              <TableCell>14 Feb 2019</TableCell>
              <TableCell className="font-medium text-green-600">$15,750</TableCell>
              <TableCell>8</TableCell>
              <TableCell>
                <Badge className="bg-green-100 text-green-800">Active</Badge>
              </TableCell>
              <TableCell>
                <Link href="/customers/00001">
                  <Button size="sm" variant="outline" className="bg-black text-white border-black hover:bg-gray-800">
                    <Eye className="w-4 h-4 mr-1" />
                    View
                  </Button>
                </Link>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell className="font-medium">00002</TableCell>
              <TableCell>
                <div className="flex items-center gap-3">
                  <Avatar className="w-8 h-8">
                    <AvatarImage src="/placeholder-user.jpg" />
                    <AvatarFallback>RP</AvatarFallback>
                  </Avatar>
                  <span className="font-medium">Rosie Pearson</span>
                </div>
              </TableCell>
              <TableCell className="text-gray-500">979 Immanuel Ferry Suite 526</TableCell>
              <TableCell>14 Feb 2019</TableCell>
              <TableCell className="font-medium text-green-600">$8,200</TableCell>
              <TableCell>3</TableCell>
              <TableCell>
                <Badge className="bg-green-100 text-green-800">Active</Badge>
              </TableCell>
              <TableCell>
                <Button size="sm" variant="outline" className="bg-black text-white border-black hover:bg-gray-800">
                  <Eye className="w-4 h-4 mr-1" />
                  View
                </Button>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell className="font-medium">00003</TableCell>
              <TableCell>
                <div className="flex items-center gap-3">
                  <Avatar className="w-8 h-8">
                    <AvatarImage src="/placeholder-user.jpg" />
                    <AvatarFallback>DC</AvatarFallback>
                  </Avatar>
                  <span className="font-medium">Darrell Caldwell</span>
                </div>
              </TableCell>
              <TableCell className="text-gray-500">8587 Frida Ports</TableCell>
              <TableCell>14 Feb 2019</TableCell>
              <TableCell className="font-medium text-green-600">$2,100</TableCell>
              <TableCell>1</TableCell>
              <TableCell>
                <Badge className="bg-red-100 text-red-800">Inactive</Badge>
              </TableCell>
              <TableCell>
                <Button size="sm" variant="outline" className="bg-black text-white border-black hover:bg-gray-800">
                  <Eye className="w-4 h-4 mr-1" />
                  View
                </Button>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </div>
  )
}
