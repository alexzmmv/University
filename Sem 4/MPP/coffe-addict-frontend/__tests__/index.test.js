import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { SearchFilterSortSection } from '../src/app/components/homeWindow/SearchFilterSortSection';
import { FilterBar } from '../src/app/components/homeWindow/FilterBar';
import { Sort } from '../src/app/components/homeWindow/Sort';

// Mock data for coffee shops
const mockCoffeeShops = [
    { id: 1, name: "Coffee Lab", rating: "4.7", distance: "0.3 km", status: "Open until 8 PM" },
    { id: 2, name: "Java Junction", rating: "4.2", distance: "1.5 km", status: "Open until 7 PM" },
    { id: 3, name: "Bean Bliss", rating: "4.9", distance: "0.8 km", status: "Closed" },
    { id: 4, name: "Espresso Express", rating: "3.8", distance: "0.2 km", status: "Open until 6 PM" },
    { id: 5, name: "Morning Brew", rating: "4.6", distance: "2.1 km", status: "Open until 9 PM" },
];

describe('FilterBar Component', () => {
    test('renders all filter options', () => {
        const mockOnFilterChange = jest.fn();
        render(<FilterBar activeFilters={[]} onFilterChange={mockOnFilterChange} />);
        
        expect(screen.getByText('Open Now')).toBeInTheDocument();
        expect(screen.getByText('4.5+')).toBeInTheDocument();
        expect(screen.getByText('Within 1 km')).toBeInTheDocument();
    });

    test('highlights active filters', () => {
        const mockOnFilterChange = jest.fn();
        render(<FilterBar activeFilters={['openNow', 'nearby']} onFilterChange={mockOnFilterChange} />);
        
        const openNowButton = screen.getByText('Open Now');
        const highRatedButton = screen.getByText('4.5+');
        const nearbyButton = screen.getByText('Within 1 km');
        
        expect(openNowButton.classList.contains('bg-amber-800')).toBeTruthy();
        expect(highRatedButton.classList.contains('bg-amber-800')).toBeFalsy();
        expect(nearbyButton.classList.contains('bg-amber-800')).toBeTruthy();
    });

    test('toggles filter when button is clicked', () => {
        const mockOnFilterChange = jest.fn();
        render(<FilterBar activeFilters={['openNow']} onFilterChange={mockOnFilterChange} />);
        
        fireEvent.click(screen.getByText('4.5+'));
        expect(mockOnFilterChange).toHaveBeenCalled();
        
        fireEvent.click(screen.getByText('Open Now'));
        expect(mockOnFilterChange).toHaveBeenCalledTimes(2);
    });
});

describe('Sort Component', () => {
    test('renders all sort options', () => {
        const mockOnSortChange = jest.fn();
        render(<Sort activeSort="rating" onSortChange={mockOnSortChange} />);
        
        expect(screen.getByText('Highest Rated')).toBeInTheDocument();
        expect(screen.getByText('Nearest First')).toBeInTheDocument();
        expect(screen.getByText('Sort by:')).toBeInTheDocument();
    });

    test('highlights the active sort option', () => {
        const mockOnSortChange = jest.fn();
        render(<Sort activeSort="rating" onSortChange={mockOnSortChange} />);
        
        const ratingButton = screen.getByText('Highest Rated');
        const distanceButton = screen.getByText('Nearest First');
        
        expect(ratingButton.classList.contains('bg-amber-800')).toBeTruthy();
        expect(distanceButton.classList.contains('bg-amber-800')).toBeFalsy();
    });

    test('calls onSortChange when a sort button is clicked', () => {
        const mockOnSortChange = jest.fn();
        render(<Sort activeSort="rating" onSortChange={mockOnSortChange} />);
        
        fireEvent.click(screen.getByText('Nearest First'));
        expect(mockOnSortChange).toHaveBeenCalledWith('distance');
        
        fireEvent.click(screen.getByText('Highest Rated'));
        expect(mockOnSortChange).toHaveBeenCalledWith('rating');
    });
});
