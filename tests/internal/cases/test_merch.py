import uuid
import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from src.internal.cases.merch import create, get, get_all, update, delete
from src.internal.entities.merch import CreateMerch, UpdateMerch
from src.db import models as m


@pytest.fixture
def mock_session():
    """Mock AsyncSession for testing."""
    session = AsyncMock(spec=AsyncSession)
    session.begin.return_value.__aenter__ = AsyncMock()
    session.begin.return_value.__aexit__ = AsyncMock(return_value=None)
    return session


@pytest.fixture
def sample_merch():
    """Sample merch data for testing."""
    return m.Merch(
        id=uuid.uuid4(),
        name="Sample Merch",
        info="This is a sample merch item",
        image_url="http://example.com/merch.jpg",
        points_needed=100
    )


@pytest.fixture
def create_merch_data():
    """Sample CreateMerch data."""
    return CreateMerch(
        name="Sample Merch",
        info="This is a sample merch item",
        image_url="http://example.com/merch.jpg",
        points_needed=100
    )


@pytest.fixture
def update_merch_data():
    """Sample UpdateMerch data."""
    return UpdateMerch(
        name="Updated Merch",
        info=None,
        image_url="http://example.com/updated_merch.jpg",
        points_needed=150
    )


class TestCreateMerch:
    @pytest.mark.asyncio
    async def test_create_merch_success(self, mock_session, sample_merch, create_merch_data):
        # Arrange
        with patch('internal.cases.merch.c.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.create_merch.return_value = sample_merch
            mock_querier_class.return_value = mock_querier

            # Act
            result = await create(mock_session, create_merch_data)

            # Assert
            assert result == sample_merch
            mock_querier.create_merch.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_merch_failure(self, mock_session, create_merch_data):
        # Arrange
        with patch('internal.cases.merch.c.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.create_merch.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await create(mock_session, create_merch_data)

            # Assert
            assert result is None
            mock_querier.create_merch.assert_called_once()


class TestGetMerch:
    @pytest.mark.asyncio
    async def test_get_merch_success(self, mock_session, sample_merch):
        # Arrange
        merch_id = sample_merch.id
        with patch('internal.cases.merch.c.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_merch_by_id.return_value = sample_merch
            mock_querier_class.return_value = mock_querier

            # Act
            result = await get(mock_session, merch_id)

            # Assert
            assert result == sample_merch
            mock_querier.get_merch_by_id.assert_called_once_with(id=merch_id)

    @pytest.mark.asyncio
    async def test_get_merch_not_found(self, mock_session):
        # Arrange
        merch_id = uuid.uuid4()
        with patch('internal.cases.merch.c.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_merch_by_id.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await get(mock_session, merch_id)

            # Assert
            assert result is None
            mock_querier.get_merch_by_id.assert_called_once_with(id=merch_id)


class TestGetAllMerch:
    @pytest.mark.asyncio
    async def test_get_all_merch(self, mock_session, sample_merch):
        # Arrange
        merch_list = [sample_merch]

        async def mock_async_iter():
            for merch in merch_list:
                yield merch

        with patch('internal.cases.merch.c.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_all_merch = mock_async_iter
            mock_querier_class.return_value = mock_querier

            # Act
            result = await get_all(mock_session)

            # Assert
            assert result == merch_list

    @pytest.mark.asyncio
    async def test_get_all_merch_empty(self, mock_session):
        # Arrange
        async def mock_async_iter():
            return
            yield  # pragma: no cover

        with patch('internal.cases.merch.c.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_all_merch = mock_async_iter
            mock_querier_class.return_value = mock_querier

            # Act
            result = await get_all(mock_session)

            # Assert
            assert result == []


class TestUpdateMerch:
    @pytest.mark.asyncio
    async def test_update_merch_success(self, mock_session, sample_merch, update_merch_data):
        # Arrange
        merch_id = sample_merch.id
        updated_merch = m.Merch(
            id=merch_id,
            name="Updated Merch",
            info=sample_merch.info,
            image_url="http://example.com/updated_merch.jpg",
            points_needed=150
        )
        with patch('internal.cases.merch.c.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.update_merch.return_value = updated_merch
            mock_querier_class.return_value = mock_querier

            # Act
            result = await update(mock_session, merch_id, update_merch_data)

            # Assert
            assert result == updated_merch
            mock_querier.update_merch.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_merch_not_found(self, mock_session, update_merch_data):
        # Arrange
        merch_id = uuid.uuid4()
        with patch('internal.cases.merch.c.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.update_merch.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await update(mock_session, merch_id, update_merch_data)

            # Assert
            assert result is None
            mock_querier.update_merch.assert_called_once()


class TestDeleteMerch:
    @pytest.mark.asyncio
    async def test_delete_merch_success(self, mock_session):
        # Arrange
        merch_id = uuid.uuid4()
        with patch('internal.cases.merch.c.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.delete_merch.return_value = None  # delete_merch doesn't return anything in the code
            mock_querier_class.return_value = mock_querier

            # Act
            result = await delete(mock_session, merch_id)

            # Assert
            assert result is True
            mock_querier.delete_merch.assert_called_once_with(id=merch_id)