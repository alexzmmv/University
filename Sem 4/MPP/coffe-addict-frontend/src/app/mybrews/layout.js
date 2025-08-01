import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
    title: 'My Brews - Coffee Addict',
    description: 'View and manage your coffee brews',
}

export default function MyBrewsLayout({ children }) {
    return (
        <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="py-8">
                {children}
            </div>
        </div>
    )
}